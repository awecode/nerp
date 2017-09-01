import React from 'react'
import Select from 'react-select'
import 'react-select/scss/default.scss'

export class ReactSelectWrapper extends React.Component {

  constructor (props) {
    super(props)
    this.onChange = this.onChange.bind(this)
    this.onBlur = this.onBlur.bind(this)
  }

  onChange (value) {
    if (value) {
      this.props.input.onChange(value.value)
    } else {
      this.props.input.onChange('')
    }
  }

  onBlur (value) {
    if (value) {
      this.props.input.onBlur(value.value)
    } else {
      this.props.input.onBlur('')
    }
  }

  render = () => {
    return (
      <div className="form-group">
        <label>
          {this.props.label}
        </label>
        <Select {...this.props}
                onBlur={this.onBlur}
                onChange={this.onChange}
                value={this.props.input.value}
        />
        {this.props.meta.touched && this.props.meta.error && <span>{this.props.meta.error}</span>}
      </div>
    )
  }
}

export const renderReactSelectWrapper = props => (<ReactSelectWrapper {...props}/>)

export const renderField = ({input, label, type, meta: {touched, error}}) =>
  <div>

    <div className="form-group">
      <label>
        {label}
      </label><br/>
      <input {...input} type={type} placeholder={label}/>
      {touched &&
      error &&
      <span>
          {error}
        </span>}
    </div>
  </div>