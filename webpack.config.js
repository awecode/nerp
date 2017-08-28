const webpack = require('webpack');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const CleanWebpackPlugin = require('clean-webpack-plugin');
const AssetsPlugin = require('assets-webpack-plugin');


const outputPath = __dirname + '/static/dist/';

// const path = require('path');


// the path(s) that should be cleaned
let pathsToClean = [outputPath];

let commonsPlugin = new webpack.optimize.CommonsChunkPlugin({name: 'common', filename: 'js/common.bundle-[hash].js'});

let extractTextPlugin = new ExtractTextPlugin({filename: 'css/[name]-[hash].css', allChunks: true})

let assetsPluginInstance = new AssetsPlugin({
  filename: 'assets.json',
  path: __dirname
})

module.exports = {
  entry:{
    app: './app/src/project/index.js'
  },
  output: {
    path: outputPath,
    publicPath: 'dist/',
    filename: "js/[name].bundle-[hash].js"
  },
  module: {
    rules: [
      {
        test: /\.js$/, // files ending with .js
        exclude: /node_modules/, // exclude the node_modules directory
        loader: 'babel-loader' // use this (babel-core) loader
      },
      {
        test: /\.s?css$/,
        use: extractTextPlugin.extract({
          fallback: "style-loader",
          use: "css-loader!sass-loader"
        })
      },
      { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader?limit=10000&mimetype=application/font-woff" },
      { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader" }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(pathsToClean),
    commonsPlugin,
    extractTextPlugin,
    assetsPluginInstance
  ]
};
