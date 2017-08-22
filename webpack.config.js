const webpack = require('webpack');
let config = {
  entry: './app/src/project/index.js',
  output: {
    filename: './static/output.js'
  },
  module: {
    rules: [{
      test: /\.js$/, // files ending with .js
      exclude: /node_modules/, // exclude the node_modules directory
      loader: "babel-loader" // use this (babel-core) loader
    }]
  },

}

module.exports = config;