const path = require('path');
const webpack = require('webpack')
const ExtractTextPlugin = require("extract-text-webpack-plugin");

var PATH = {
  "index": path.join(__dirname, 'app', 'src')
};

const extractSass = new ExtractTextPlugin({
    filename: "[name].[contenthash].css",
    disable: process.env.NODE_ENV === "development"
});

let config = {
  entry: './app/src/project/index.js',
  output: {
    filename: './static/output.js'
  },
  module: {
    rules: [
      {
        test: /\.js$/, // files ending with .js
        exclude: /node_modules/, // exclude the node_modules directory
        loader: 'babel-loader' // use this (babel-core) loader
      },
      {
        test: /\.scss$/,
        use: extractSass.extract({
                use: [{
                    loader: "css-loader", options:{
                      sourceMap: true
                  }
                }, {
                    loader: "sass-loader", options:{
                      sourceMap: true
                  }
                }],
                // use style-loader in development
                fallback: "style-loader"
            })
      }
    ]
  },
  plugins: [
        extractSass
    ]

}

module.exports = config