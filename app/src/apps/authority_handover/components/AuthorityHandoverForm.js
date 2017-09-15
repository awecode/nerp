import React from 'react'
import { Field, FieldArray, reduxForm } from 'redux-form'
import { renderField, renderReactSelectWrapper } from '../../../project/components/ReduxFormFieldComponents'
import { renderBudgetDistributions } from './BudgetDistributionForm'
import { getOptions } from '../../server_data/actions/query'

// todo translation

let validate = (form_data) =>
{
  console.log(form_data)
}

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
  authority_handover_type = [
    {value: 'first', label: 'First'},
    {value: 'addition', label: 'Addition'},
    {value: 'edited', label: 'Edited'},
  ]

  render () {
    return (
      <div className="card">
        <div className="card-block">

          <form>
            <div className="row">
              <div className="col-md-2">
                <label>Handover Type</label>
              </div>
              <div className="col-md-2">
                <Field name="type" component={renderReactSelectWrapper}
                       options={this.authority_handover_type}
                       label="Handover Type"
                />
              </div>
              <div className="col-md-2">
                <label>Parent Handover</label>
              </div>
              <div className="col-md-2">
                <Field name="parent" component={renderReactSelectWrapper}
                       options={getOptions('authority_handover', 'authority_handover', '/api/v1/authority-handover/choices/')}
                       label="Parent Handover"
                />
              </div>
              <div className="col-md-2">
                <label>Beneficiary Office</label>
              </div>
              <div className="col-md-2">
                <Field name="beneficiary" component={renderReactSelectWrapper}
                       options={getOptions('authority_handover', 'beneficiary', '/api/v1/beneficiary/choices/')}
                       label="Beneficiary Office"
                />
              </div>
            </div>
            <div className="row">
              <div className="col-md-2">
                <label>Fiscal Year</label>
              </div>
              <div className="col-md-2">
                <Field name="fiscal_year" component={renderReactSelectWrapper}
                       options={getOptions('core', 'fiscal_year', '/api/v1/fiscal-year/choices/')}
                       label="Fiscal Year"
                />
              </div>
              <div className="col-md-2">
                <label>Budget Head</label>
              </div>

              <div className="col-md-2">
                <Field name="budget_head" component={renderReactSelectWrapper}
                       options={getOptions('core', 'budget_head', '/api/v1/budget-head/choices/')}
                       label="Budget Head"
                />
              </div>
              <div className="col-md-2">
                <label>Priority Code</label>
              </div>
              <div className="col-md-2">
                <Field name="priority_code" type="text" label="Priority" component={renderField}/>
              </div>
            </div>
            <div className="row">
              <div className="col-md-2">
                <label>Date</label>
              </div>
              <div className="col-md-2">
                <Field name="date" type="date" label="Date" component={renderField}/>
              </div>
            </div>
            <hr/>
            <div className="mt-3">
              <FieldArray name="budget_distributions" component={renderBudgetDistributions}/>
            </div>
          </form>
        </div>
      </div>
    )
  }
}

const AuthorityHandover = reduxForm({
  // a unique name for the form
  form: 'authority_handover',
  validate
})(AuthorityHandoverForm)

export default AuthorityHandover