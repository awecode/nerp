import React from 'react'
import { Field, reduxForm } from 'redux-form'
import Select from 'react-select'
import { renderReactSelectWrapper } from '../../../project/utils/ReduxFormSelect'

// todo translation

class AuthorityHandoverForm extends React.Component {
  fund_sub_type= [
        {value: 'cash', label: 'Cash'},
        {value: 'reimbursable', label: 'Reimbursable'},
        {value: 'direct payment', label: 'Direct Payment'},
        {value: 'commodity', label: 'Commodity'}
      ]

  render () {
    return (
      <form>
        <div>
          <label htmlFor="parent">Parent</label>
          <Field name="parent" component={renderReactSelectWrapper}
                 options={this.fund_sub_type}
          />
        </div>
        <div>
          <label htmlFor="beneficiary">Beneficiary Office</label>
          <Field name="beneficiary" component={renderReactSelectWrapper} options={this.fund_sub_type} />
        </div>
        <div>
          <label htmlFor="fiscal_year">Fiscal Year</label>
          <Field name="fiscal_year" component={renderReactSelectWrapper} options={this.fund_sub_type} />
        </div>
        <div>
          <label htmlFor="budget_head">Budget Head</label>
          <Field name="budget_head" component={renderReactSelectWrapper} options={this.fund_sub_type} />
        </div>
        <div>
          <label htmlFor="priority">Priority</label>
          <Field name="priority" component="input" type="text"/>
        </div>
      </form>
    )
  }
}

const AuthorityHandover = reduxForm({
  // a unique name for the form
  form: 'authority_handover'
})(AuthorityHandoverForm)

export default AuthorityHandover