package com.example.nguyenmanhduc.foodtrail;

import android.content.IntentSender;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.location.Location;
import android.os.AsyncTask;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.support.annotation.Nullable;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.places.Places;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback,
        GoogleApiClient.ConnectionCallbacks,
        GoogleApiClient.OnConnectionFailedListener,
        LocationListener, View.OnClickListener {

    private GoogleMap mMap;
    private final int zoomLevel = 15;
    private GoogleApiClient mGoogleApiClient;
    public static final String TAG = MapsActivity.class.getSimpleName();

    private final static int CONNECTION_FAILURE_RESOLUTION_REQUEST = 9000;
    private LocationRequest mLocationRequest;
    private static final int REQUEST_LOCATION = 2;
    private Location location;
    private Button place_marker;
    private Button undo_marker;

    private LatLng start_pos;
    private LatLng end_pos;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);

        place_marker = (Button) findViewById(R.id.place_marker);
        place_marker.setOnClickListener(this);
        undo_marker = (Button) findViewById(R.id.undo_button);
        undo_marker.setOnClickListener(this);

        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addApi(LocationServices.API)
                .addApi(Places.GEO_DATA_API)
                .addApi(Places.PLACE_DETECTION_API)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .build();

        mLocationRequest = LocationRequest.create()
                .setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY)
                .setInterval(1000)
                .setFastestInterval(100);
    }

    @Override
    public void onClick(View view) {
        /* Can add other buttons and switch among them by view Id */
        switch (view.getId()) {
            /* Click on the place marker button */
            case (R.id.place_marker):
                LatLng center = mMap.getCameraPosition().target;
                placeMarkerOnMapCenter(center);
                /* If the start position has been set, change to finish marker text
                 on the button */
                if(start_pos == null) {
                    start_pos = center;
                    place_marker.setText(R.string.finish_marker_text);

                } else if (end_pos == null){
                    // Perform google map query and draw the polyline on UI
                    end_pos = center;
                    findDirection(start_pos, end_pos);
                }
                break;
            case (R.id.undo_button):
                mMap.clear();
                place_marker.setText("Start");
                start_pos = null;
                end_pos = null;
                break;
            default:
                break;
        }
    }

    private void placeMarkerOnMapCenter(LatLng center) {
        mMap.addMarker(new MarkerOptions().position(center).icon(BitmapDescriptorFactory.fromResource(R.drawable.center_marker)));
    }

    private void findDirection(LatLng start, LatLng finish) {
        /* Create a HTTP query to pass into FetchURL
        * The results of the request will be processed and poly-lines
        * will be added in the Parser class
        */
        String start_cd = Double.toString(start.latitude)+","+Double.toString(start.longitude);
        String finish_cd =  Double.toString(finish.latitude)+","+Double.toString(finish.longitude);
        String url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + start_cd
                + "&destination=" + finish_cd;
        FetchURL direction_query = new FetchURL();
        direction_query.execute(url);
    }

    @Override
    protected void onStart() {
        super.onStart();
        mGoogleApiClient.connect();
    }

    @Override
    protected void onStop() {
        mGoogleApiClient.disconnect();
        super.onStop();
    }

    @Override
    protected void onResume() {
        super.onResume();
        mGoogleApiClient.connect();
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (mGoogleApiClient.isConnected()) {
            LocationServices.FusedLocationApi.removeLocationUpdates(mGoogleApiClient, this);
            mGoogleApiClient.disconnect();
        }
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED
                && ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            return;
        }
        mMap.setMyLocationEnabled(true);
        mMap.setOnMyLocationButtonClickListener(new GoogleMap.OnMyLocationButtonClickListener() {
            @Override
            public boolean onMyLocationButtonClick() {
                performLocationUpdates();
                return true;
            }
        });
    }

    @Override
    public void onConnected(@Nullable Bundle bundle) {
        if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED
                && ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION},
                    REQUEST_LOCATION);
        } else {
            location = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);
            if (location == null) {
                performLocationUpdates();
            }
            else {
                handleNewLocation(location);
            };
        }
    }

    private void performLocationUpdates(){
        LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient, mLocationRequest, this);
    }

    @Override
    public void onLocationChanged(Location location)
    {
        handleNewLocation(location);
    }

    private void handleNewLocation(Location location) {
        double currentLatitude = location.getLatitude();
        double currentLongitude = location.getLongitude();
        LatLng latLng = new LatLng(currentLatitude, currentLongitude);
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(latLng, zoomLevel));
    }

    @Override
    public void onConnectionSuspended(int i) {
        Log.i(TAG, "Location services suspended. Please reconnect.");
    }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
        if (connectionResult.hasResolution()) {
            try {
                connectionResult.startResolutionForResult(this, CONNECTION_FAILURE_RESOLUTION_REQUEST);
            } catch (IntentSender.SendIntentException e) {
                e.printStackTrace();
            }
        } else {
            Log.i(TAG, "Location services connection failed with code " + connectionResult.getErrorCode());
        }
    }

    /*
     Private class FetchURL to perform HTTP request to the google direction API
     Flow:
      - FetchURL makes HTTP request to google direction API in the background
      - Once this result returns, pass it to PostExecute
      - Invokes a parser class that parses the JSON result (in background)
      (using a DataParser class)
      - Returned results is added to the google map
     */
    private class FetchURL extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... url) {
            String data = "";
            try{
                data = downLoadURL(url[0]);
            } catch (Exception e) {
                e.printStackTrace();
            }
            return data;
        }

        @Override
        protected void onPostExecute(String data) {
            super.onPostExecute(data);
            Parser parser = new Parser();
            parser.execute(data);
        }
    }

    private String downLoadURL(String strURL) throws IOException {
        String data = "";
        InputStream iStream = null;
        HttpURLConnection connection = null;
        try{
            URL url = new URL(strURL); /* Make an url connection */
            connection = (HttpURLConnection) url.openConnection();
            connection.connect();
            iStream = connection.getInputStream(); /* Get the return connection stream */
            BufferedReader br = new BufferedReader(new InputStreamReader(iStream));
            StringBuffer sb = new StringBuffer();
            String line;
            /* Read line by line */
            while ((line = br.readLine()) != null) {
                sb.append(line);
            }
            data = sb.toString();
            br.close();
        } catch (Exception e) {
            Log.d(TAG, e.toString());
        } finally {
            if(iStream != null) iStream.close();
            connection.disconnect();
        }
        return data;
    }

    /* This class parses the json data from download url */
    private class Parser extends AsyncTask<String, Integer, List<List<HashMap<String, Double>>>>{
        private String base_request =
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?type=restaurant&key=AIzaSyCDTI-HFdYvXK5vIkEH159grYMBlwepkbw&rankby=prominence";

        @Override
        protected List<List<HashMap<String, Double>>> doInBackground(String... jData) {
            JSONObject jobject;
            List<List<HashMap<String, Double>>> routes = null;
            try {
                jobject = new JSONObject(jData[0]);
                DataParser parser = new DataParser();
                routes = parser.parse(jobject);
            } catch (Exception e) {
                e.printStackTrace();
            }
            return routes;
        }

        @Override
        protected void onPostExecute (List<List<HashMap<String, Double>>> result) {
            ArrayList<LatLng> points = new ArrayList<>();
            ArrayList<HashMap<String, Double>> placesReqInfo = new ArrayList<>();
            PolylineOptions lineOptions = new PolylineOptions();

            /* There is only one route, get the first route */
            for (int i = 0; i < result.size(); i++) {
                // Get each step
                List<HashMap<String, Double>> path = result.get(i);
                // Get the 'summary' hm
                placesReqInfo.add(path.get(0));
                // Use the mLat/mLng -> send a request to google places api

                for (int j = 1; j < path.size(); j++) {
                    HashMap<String, Double> point = path.get(j);
                    double lat = point.get("lat");
                    double lng = point.get("lng");
                    LatLng position = new LatLng(lat, lng);
                    points.add(position);
                }
            }
            lineOptions.addAll(points).width(10).color(Color.RED);

            if (lineOptions != null) {
                mMap.addPolyline(lineOptions);
            }

            if (placesReqInfo != null) {
                // Loop through the array of LatLngs to query for the surrounding restaurant
                for (int i = 0; i < placesReqInfo.size(); i++) {
                    HashMap<String, Double> midLoc = placesReqInfo.get(i);
                    Double mLat = midLoc.get("mlat");
                    Double mLng = midLoc.get("mlng");
                    Double radius = midLoc.get("dist")/2;

                    String apiRequest = base_request + "&location=" + Double.toString(mLat) + ","
                            + Double.toString(mLng) + "&radius=" + Double.toString(radius);
                    GGPlacesAPI request = new GGPlacesAPI();
                    request.execute(apiRequest);
                }
            }
        }

        private class GGPlacesAPI extends AsyncTask<String, Void, String> {
            @Override
            protected String doInBackground(String... url) {
                String data = "";
                try {
                    data = downLoadURL(url[0]);
                } catch (Exception e) {
                    e.printStackTrace();
                }
                return data;
            }

            protected void onPostExecute(String data) {
                JSONObject place_data = null;
                JSONArray result;
                try {
                    place_data = new JSONObject(data);
                } catch (Exception e) {
                    Log.d(TAG, e.toString());
                }
                if (place_data != null) {
                    try {
                        result = place_data.getJSONArray("results");
                        /* Limit to top 5 results */
                        for (int i = 0; i < result.length() && i < 5; i++) {
                            try {
                                String address = (String) ((JSONObject) result.get(i))
                                        .get("vicinity");
                                JSONObject geometry = (JSONObject) ((JSONObject) result.get(i))
                                        .get("geometry");

                                JSONObject location = (JSONObject) geometry.get("location");

                                /* Retrieve the name/lat/lng info */
                                String name = (String) ((JSONObject) result.get(i))
                                        .get("name");
                                double lat = (Double) location.get("lat");
                                double lng = (Double) location.get("lng");

                                place_map_marker(name, lat, lng, address);

                            } catch (JSONException e) {
                                Log.d(TAG, e.toString());
                            }
                        }
                    } catch (JSONException e) {
                        Log.d(TAG, e.toString());
                    }
                }
            }
        }

        private void place_map_marker(String name, double lat, double lng, String address) {
            LatLng marker = new LatLng(lat, lng);
            mMap.addMarker(new MarkerOptions().position(marker).title(name).snippet(address)
                    .icon(BitmapDescriptorFactory.fromResource(R.drawable.restaurant_marker)));
        }
    }
}
