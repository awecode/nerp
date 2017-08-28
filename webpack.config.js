const path = require('path')
const process = require('process')
const webpack = require('webpack')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const AssetsPlugin = require('assets-webpack-plugin')

const PATH = {
  'src': path.join(__dirname, 'app', 'src'),
  'static': path.join(__dirname, 'static', 'webpack'),
}

const assetsPluginInstance = new AssetsPlugin({
  filename: 'assets.json',
  path: path.join(__dirname)
})

const extractSass = new ExtractTextPlugin({
  filename: '[name].[chunkhash].css',
  disable: process.env.NODE_ENV === 'development'
})

const provide = new webpack.ProvidePlugin({
  jQuery: 'jquery',
  $: 'jquery',
  jquery: 'jquery',
  'window.jQuery': 'jquery',
  Popper: 'popper.js',
  Tether: 'tether'
})

const commonChunkPlugin = new webpack.optimize.CommonsChunkPlugin({
  name: 'common',
  filename: 'common.[chunkhash].bundle.js'
})

let config = {
  entry: {
    index: './app/src/project/index.js',
    common: [
      'react',
      'react-dom',
      'react-redux',
      'redux-form',
      'react-router-dom',
      'jquery',
      'popper.js',
      'bootstrap'
    ]
  },
  output: {
    path: PATH['static'],
    filename: '[name].[chunkhash].bundle.js',
    publicPath: 'webpack/'
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.js$/, // files ending with .js
        exclude: /node_modules/, // exclude the node_modules directory
        loader: 'babel-loader' // use this (babel-core) loader
      },
      {
        test: /\.(scss)$/,
        use: extractSass.extract({
          use: [{
            loader: 'css-loader', options: {
              sourceMap: true,
              minimize: true
            }
          }, {
            loader: 'sass-loader', options: {
              sourceMap: true,
              minimize: true
            }
          }],
          // use style-loader in development
          fallback: 'style-loader'
        })
      }
    ]
  },
  plugins: [
    provide,
    extractSass,
    commonChunkPlugin,
    assetsPluginInstance
  ]

}

module.exports = config