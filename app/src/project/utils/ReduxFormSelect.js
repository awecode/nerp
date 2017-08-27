import React from 'react'
import { Field } from 'redux-form'
import Select from 'react-select'
import 'react-select/scss/default.scss';

export class ReactSelectWrapper extends React.Component {

  constructor(props) {
    super(props);
  }

  render = () => {

    return (<Select {...this.props}/>);
  }

}

export const renderReactSelectWrapper = props => (<ReactSelectWrapper {...props}/>);