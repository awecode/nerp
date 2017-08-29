import React from 'react'
import Select from 'react-select'
import 'react-select/scss/default.scss'

export class ReactSelectWrapper extends React.Component {

  constructor (props) {
    super(props)
    this.onChange = this.onChange.bind(this)
    this.onBlur = this.onBlur.bind(this)
  }

  onChange(value){
    this.props.input.onChange(value.value)
  }

  onBlur(value){
     this.props.input.onBlur(value.value)
  }

  render = () => {

    return (
      <div>
      <Select {...this.props}
              onBlur={this.onBlur}
              onChange={this.onChange}
              value={this.props.input.value}
      />
      {this.props.meta.touched && this.props.meta.error && <div>{this.props.meta.error}</div>}
      </div>
    )
  }

}

export const renderReactSelectWrapper = props => (<ReactSelectWrapper {...props}/>)