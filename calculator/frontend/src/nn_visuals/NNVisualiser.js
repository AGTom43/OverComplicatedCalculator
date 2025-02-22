import rough from 'roughjs';
import Color from 'color';

/*! *****************************************************************************
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0

THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
MERCHANTABLITY OR NON-INFRINGEMENT.

See the Apache Version 2.0 License for specific language governing permissions
and limitations under the License.
***************************************************************************** */

var __assign = function() {
    __assign = Object.assign || function __assign(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};

function __rest(s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) if (e.indexOf(p[i]) < 0)
            t[p[i]] = s[p[i]];
    return t;
}

var getLines = function (_a) {
    var layer = _a.layer, cells = _a.cells, previousLayerCells = _a.previousLayerCells;
    var lines = [];
    if (!previousLayerCells) {
        return lines;
    }
    for (var i = 0; i < cells.length; i++) {
        for (var j = 0; j < previousLayerCells.length; j++) {
            var cell = cells[i];
            var previousCell = previousLayerCells[j];
            var points = [
                cell,
                previousCell,
            ];
            var line = {
                layer: layer,
                points: points,
            };
            lines.push(line);
        }
    }
    return lines;
};

// var Color = require('color');
var COLORS = [
    Color.hsl([199, 100, 57]),
    Color.hsl([33, 100, 50]),
];
var DEFAULT_DIAMETER = 84;
var EXTRA_PADDING = 5;
var DEFAULT_FILL = 'rgb(255,255,255)';
var DEFAULT_FILL_WEIGHT = 5;
var DEFAULT_FILL_STYLE = 'solid';
var DEFAULT_STROKE_WIDTH = 3;
var DEFAULT_LINE_WIDTH = 3;
var DEFAULT_ROUGHNESS = 0.5;
var DEFAULT_BOWING = 0;

var getPosition = function (index, size, len) {
    if (len === 1) {
        return size / 2;
    }
    var total = len - 1;
    var mult = (size / total);
    return mult * index;
};

var getRange = function (num, orig, target) {
    var perc = (num - orig[0]) / (orig[1] - orig[0]);
    return perc * (target[1] - target[0]) + target[0];
};

var getCellPosition = function (_a) {
    var i = _a.i, strokeWidth = _a.strokeWidth, diameter = _a.diameter, maxCells = _a.maxCells, vertical = _a.vertical, layerPosition = _a.layerPosition, layerSize = _a.layerSize, units = _a.units;
    var extraAmount = 1200 / (Math.pow(maxCells, 2));
    var extraPadding = extraAmount * (maxCells - units);
    var pad = (diameter * .5 + strokeWidth + EXTRA_PADDING) + extraPadding;
    var position = getRange(getPosition(i, layerSize, units), [0, layerSize], [pad, layerSize - pad]);
    if (vertical) {
        return {
            x: position,
            y: layerPosition,
        };
    }
    return {
        x: layerPosition,
        y: position,
    };
};
var getCells = function (_a) {
    var units = _a.units, layer = _a.layer, props = __rest(_a, ["units", "layer"])
    // diameter,
    // maxCells,
    // layerPosition,
    // layerSize,
    // vertical,
    // strokeWidth,
    ;
    var points = [];
    for (var i = 0; i < units; i++) {
        var position = getCellPosition(__assign({ i: i,
            units: units,
            layer: layer }, props));
        points.push(__assign({ layer: layer }, position));
    }
    return points;
};

var getLayer = function (_a) {
    var layer = _a.index, layerPosition = _a.layerPosition, maxCells = _a.maxCells, layerSize = _a.layerSize, vertical = _a.vertical, _b = _a.layer, units = _b.units, diameter = _b.diameter, strokeWidth = _b.strokeWidth, previousLayerCells = _a.previousLayerCells;
    var cells = getCells({
        strokeWidth: strokeWidth,
        units: parseInt("" + units, 10),
        layer: layer,
        diameter: diameter,
        layerPosition: layerPosition,
        maxCells: maxCells,
        layerSize: layerSize,
        vertical: vertical,
    });
    var lines = getLines({
        layer: layer,
        cells: cells,
        previousLayerCells: previousLayerCells,
    });
    return {
        cells: cells,
        lines: lines,
    };
};

var getCellsAndLines = function (_a) {
    var _b = _a.network, layers = _b.layers, vertical = _b.vertical, width = _a.width, height = _a.height, props = __rest(_a, ["network", "width", "height"]);
    var maxCells = layers.reduce(function (max, layer) {
        var units = parseInt("" + layer.units, 10);
        return max < units ? units : max;
    }, 0);
    var size = vertical ? height : width;
    var previousLayerCells = null;
    var start = (layers[0].diameter / 2) + layers[0].strokeWidth + EXTRA_PADDING;
    var lastLayer = layers[layers.length - 1];
    var end = size - ((lastLayer.diameter / 2) + lastLayer.strokeWidth) - EXTRA_PADDING;
    return layers.reduce(function (obj, layer, index) {
        var layerPosition = getRange(getPosition(index, size, layers.length), [0, size], [start, end]);
        var _a = getLayer(__assign({ index: index,
            layerPosition: layerPosition,
            maxCells: maxCells, layerSize: vertical ? width : height, vertical: vertical,
            layer: layer,
            previousLayerCells: previousLayerCells }, props)), cells = _a.cells, 
        // Component,
        lines = _a.lines;
        previousLayerCells = cells;
        return {
            lines: obj.lines.concat(lines),
            cells: obj.cells.concat(cells),
        };
    }, {
        lines: [],
        cells: [],
    });
};

var parseProps = function (_a) {
    var network = _a.network, props = __rest(_a, ["network"]);
    return (__assign({}, props, { network: __assign({}, network, { layers: network.layers.map(function (layer) { return (__assign({}, layer, { diameter: layer.diameter || network.diameter || DEFAULT_DIAMETER, fill: layer.fill || network.fill || DEFAULT_FILL, fillWeight: layer.fillWeight || network.fillWeight || DEFAULT_FILL_WEIGHT, fillStyle: layer.fillStyle || network.fillStyle || DEFAULT_FILL_STYLE, strokeWidth: layer.strokeWidth || network.strokeWidth || DEFAULT_STROKE_WIDTH, lineWidth: layer.lineWidth || network.lineWidth || DEFAULT_LINE_WIDTH, roughness: layer.roughness || network.roughness || DEFAULT_ROUGHNESS, bowing: layer.bowing || network.bowing || DEFAULT_BOWING })); }) }) }));
};
var NNVisualizer = /** @class */ (function () {
    function NNVisualizer(target, props) {
        var _this = this;
        this.animating = false;
        var ind = 0;
        this.render = function (roughness) {
            var rc = rough.canvas(_this.canvas);
            _this.lines.forEach(function (line) {
                var layer = _this.network.layers[line.layer];
                rc.line(line.points[0].x, line.points[0].y, line.points[1].x, line.points[1].y, __assign({}, layer, { roughness: roughness || layer.roughness, strokeWidth: layer.lineWidth }));
            });
            _this.cells.forEach(function (cell,index) {
                var layer = _this.network.layers[cell.layer];
                if (Array.isArray(layer.fill)){
                    layer = {...layer,fill:layer.fill[ind]}; 
                    ind += 1;
                    if (ind == layer.units){
                        ind = 0;
                    }
                }
                rc.circle(cell.x, cell.y, layer.diameter, __assign({}, layer, { roughness: roughness || layer.roughness }));
            });
        };
        this.animate = function (_a) {
            var _b = _a === void 0 ? {} : _a, animateInterval = _b.animateInterval, roughness = _b.roughness;
            _this.animating = true;
            var render = function () {
                _this.render(getRand(roughness));
                setInterval(function () {
                    render();
                }, animateInterval || 100);
            };
            render();
        };
        this.stopAnimating = function () {
            _this.animating = false;
        };
        var width = props.width, height = props.height;
        this.canvas = document.createElement('canvas');
        this.canvas.width = width;
        this.canvas.height = height;
        var deviceScaleFactor = props.deviceScaleFactor || 1;
        this.canvas.style.width = width / deviceScaleFactor + "px";
        this.canvas.style.height = height / deviceScaleFactor + "px";
        this.canvas.getContext('2d').scale(deviceScaleFactor, deviceScaleFactor);
        target.appendChild(this.canvas);
        var parsedProps = parseProps(props);
        this.network = parsedProps.network;
        var _a = getCellsAndLines(parsedProps), lines = _a.lines, cells = _a.cells;
        this.lines = lines;
        this.cells = cells;
        this.render();
    }
    return NNVisualizer;
}());
var getRand = function (range) { return range[0] + (Math.random() * (range[1] - range[0])); };

export default NNVisualizer;
