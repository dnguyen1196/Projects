(function() {
                // selectAll (non existing p) and append data

        var dataset = [ 5, 10, 13, 19, 21, 25, 22, 18, 15, 13,
                        11, 12, 15, 20, 18, 17, 16, 18, 23, 25 ];

        var w = 500;
        var h = 200;
        var barPadding = 1;

        var svg = d3.select("#visualization").append("svg")
                .attr("width", w)
                .attr("height", h);

        var barw = 20;

        svg.selectAll("rect").data(dataset)
                .enter()
                .append("rect")
                .attr("x", function(d, i){
                        return i * (w / dataset.length);
                })
                .attr("y", function(d) {
                        return h - d*6;
                })
                .attr("width", w/dataset.length - barPadding)
                .attr("height", function(d) {
                        return d * 10;
                }).attr("fill", "blue");

        svg.selectAll("text").data(dataset)
                .enter()
                .append("text")
                .text(function(d){
                        return d;
                })
                .attr("x", function(d, i){
                        return i * (w / dataset.length) + (w / dataset.length - barPadding) / 2;
                })
                .attr("y", function(d, i){
                        return h - (d * 10) + (d*6);
                })
                .attr("font-family", "sans-serif")
                .attr("font-size", "11px")
                .attr("fill", "white")
                .attr("text-anchor", "middle");


}());
