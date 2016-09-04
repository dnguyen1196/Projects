package com.example.nguyenmanhduc.foodtrail;

import android.util.Log;

import com.google.android.gms.cast.LaunchOptions;
import com.google.android.gms.maps.model.LatLng;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/*
 * Created by nguyenmanhduc on 7/17/16.
 */
public class DataParser {
    public List<List<HashMap<String, Double>>> parse(JSONObject jObject) {
        List<List<HashMap<String, Double>>> routes = new ArrayList<>();
        JSONArray jRoutes;
        JSONArray jLegs;
        JSONArray jSteps;

        try {
            jRoutes = jObject.getJSONArray("routes"); // Get the field "routes"
            for (int i = 0; i < jRoutes.length(); i++) { // Get all route (1 in this case)
                jLegs = ((JSONObject) jRoutes.get(i)).getJSONArray("legs");
                for (int j = 0; j < jLegs.length(); j++) { // Get all legs (1 in this case)
                    jSteps = ((JSONObject) jLegs.get(j)).getJSONArray("steps");
                    for (int k = 0; k < jSteps.length(); k++) { // Get each step one by one
                        List path = new ArrayList();
                        // Get an individual step JSON
                        JSONObject step_array = (JSONObject) jSteps.get(k);

                        // Polyline -> JSONObject containing a field called "points"
                        // This is the encoded polyline string
                        String polyline = (String)((JSONObject)step_array.get("polyline"))
                                .get("points");

                        // Get the distance and lat/lng of start and end location
                        // -> calculate midlat and midlng
                        double distance = (double)((Integer) ((JSONObject)step_array
                                .get("distance")).get("value"));
                        double mid_lat = ((double)((JSONObject)step_array.get("start_location"))
                                .get("lat")
                                + (double)((JSONObject)step_array.get("end_location"))
                                .get("lat"))/2;
                        double mid_lng = ((double)((JSONObject)step_array.get("start_location"))
                                .get("lng")
                                + (double)((JSONObject)step_array.get("end_location"))
                                .get("lng"))/2;

                        // Decode the polyline into a series of LatLng coordinates
                        List<LatLng> list = decodePolyline(polyline);

                        // Add the 'summary' hash-map of each step
                        HashMap<String, Double> hm = new HashMap<>();
                        hm.put("dist", distance);
                        hm.put("mlat", mid_lat);
                        hm.put("mlng", mid_lng);
                        path.add(hm);

                        for (int l = 0; l < list.size(); l++) {
                            HashMap<String, Double> polycoord = new HashMap<>();
                            polycoord.put("lat", (list.get(l)).latitude);
                            polycoord.put("lng", (list.get(l)).longitude);
                            path.add(polycoord);
                        }
                        routes.add(path);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return routes;
    }

    /*
    Function to decode the polyline string returned by google direction api
     */
    public List<LatLng> decodePolyline(String polyline) {
        List<LatLng> line = new ArrayList<>();
        int index = 0;
        int len = polyline.length();
        int lat = 0, lng = 0;

        while (index < len) {
            int b, shift = 0, result = 0;
            do {
                b = polyline.charAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            int dlat = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
            lat += dlat;
            shift = 0;
            result = 0;
            do {
                b = polyline.charAt(index++) -  63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            int dlng = ((result & 1) != 0) ? ~(result >> 1) : (result >> 1);
            lng += dlng;

            LatLng p = new LatLng((double) lat/1E5, (double) lng / 1E5);
            line.add(p);
        }
        return line;
    }
}
