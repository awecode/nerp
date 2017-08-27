import React from 'react'

class ForeignFundForm extends React.Component {

  fund_type = ['grant', 'loan'];

  render () {
    return (
      <div>
          <Field name="fund_type" component="select">
            <option></option>
            <option value="#ff0000">Red</option>
            <option value="#00ff00">Green</option>
            <option value="#0000ff">Blue</option>
          </Field>
          <Field name="fund_sub_type" component="select">
            <option></option>
            <option value="#ff0000">Red</option>
            <option value="#00ff00">Green</option>
            <option value="#0000ff">Blue</option>
          </Field>

        </div>
      </div>
    )
  }
}

// No need to connect()!
export default ForeignFundForm