import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'

import { BrowserRouter as Router } from 'react-router-dom'
import AppRoute from './Route'
// import ScrollToTop from './ScrollToTop';
import { store } from './store'

import './bootstrap'

import './scss/project.scss'

if (window.init_actions) {
  window.init_actions.forEach(
    action => {
      store.dispatch(action)
    }
  )
}

ReactDOM.render(
  <Provider store={store}>
    <Router>
      <AppRoute/>
    </Router>
  </Provider>,
  document.getElementById('app')
)