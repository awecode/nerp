import React from 'react'
import { Field, reduxForm } from 'redux-form'
import Select from 'react-select'
import { renderReactSelectWrapper } from '../../../project/utils/ReduxFormSelect'

// todo translation

class AuthorityHandoverForm extends React.Component {
  // constructor(props){
  //   super(props)
  // }



  fund_sub_type = [
    {value: 'cash', label: 'Cash'},
    {value: 'reimbursable', label: 'Reimbursable'},
    {value: 'direct payment', label: 'Direct Payment'},
    {value: 'commodity', label: 'Commodity'}
  ]
  sub_type = [
    {value: 'cash', label: 'Cash'},
    {value: 'reimbursable', label: 'Reimbursable'},
    {value: 'direct payment', label: 'Direct Payment'},
    {value: 'commodity', label: 'Commodity'}
  ]


  render () {
    return (
      <form>
        <div className="row">
          <div className="col-sm-6 col-md-3">
            <label htmlFor="parent">Parent</label>
            <Field name="parent" component={renderReactSelectWrapper}
                   options={this.fund_sub_type}
            />
          </div>
          <div className="col-sm-6 col-md-3">
            <label htmlFor="beneficiary">Beneficiary Office</label>
            <Field name="beneficiary" component={renderReactSelectWrapper}
                   options={this.sub_type}
            />
          </div>
          <div className="col-sm-6 col-md-3">
            <label htmlFor="fiscal_year">Fiscal Year</label>
            <Field name="fiscal_year" component={renderReactSelectWrapper} options={this.fund_sub_type}/>
          </div>
          <div className="col-sm-6 col-md-3">
            <label htmlFor="budget_head">Budget Head</label>
            <Field name="budget_head" component={renderReactSelectWrapper} options={this.fund_sub_type}/>
          </div>
          <div className="col-sm-6 col-md-3">
            <label htmlFor="priority">Priority</label><br/>
            <Field name="priority" component="input" type="text"/>
          </div>
        </div>
        <div className="row">
          <div>

          </div>
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