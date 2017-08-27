import React from 'react'
import Select from 'react-select'

class ForeignFundForm extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      fund_sub_type: [
        {value: 'cash', label: 'Cash'},
        {value: 'reimbursable', label: 'Reimbursable'},
        {value: 'direct payment', label: 'Direct Payment'},
        {value: 'commodity', label: 'Commodity'}
      ],
      // donors: this.props.donors
    }
    this.handleInputChange = this.handleInputChange.bind(this)
  }

  handleInputChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;

    // this.setState({
    //   [name]: value
    // });

  }

  render () {

    return (
      <div>
        <Select
          name="form-field-name"
          value="one"
          options={this.state.fund_sub_type}
          onChange={this.handleInputChange}
        />
        <Select
          name="form-field-name"
          value="one"
          options={this.state.fund_sub_type}
          onChange={this.handleInputChange}
        />
        <Field name="amount" component="text"/>
      </div>
    )
  }
}

// No need to connect()!
export default ForeignFundForm