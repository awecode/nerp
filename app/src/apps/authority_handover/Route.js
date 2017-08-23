import React from 'react';
import {Route, Switch} from 'react-router-dom';
import AuthorityHandoverForm from './components/AuthorityHandoverForm'

// import {App} from './RouteSync'


class AppRoute extends React.Component {
  render() {
    return (
      <div>
        <AuthorityHandoverForm/>
      </div>
    )
  }
}

export default AppRoute;