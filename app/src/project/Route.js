import React from 'react'
import { Route, Switch } from 'react-router-dom'
import AuthorityHandover from '../apps/authority_handover/index'
import Header from './components/Header'
import Footer from './components/Footer'

// import { Footer, Header } from './RouteSync'

class AppRoute extends React.Component {
  render () {
    return (
      <div>
        <Header/>
        <div className="container-fluid">
          <AuthorityHandover/>
        </div>
        <Footer/>
      </div>
    )
  }
}

export default AppRoute