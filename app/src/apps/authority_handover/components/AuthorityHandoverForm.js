import React from 'react'
import { Field, FieldArray, reduxForm } from 'redux-form'
import { renderField, renderReactSelectWrapper } from '../../../project/components/ReduxFormFieldComponents'
import { renderBudgetDistributions } from './BudgetDistributionForm'
import { getOptions } from '../../server_data/actions/query'

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
  authority_handover_type = [
    {value: 'first', label: 'First'},
    {value: 'addition', label: 'Addition'},
    {value: 'edited', label: 'Edited'},
  ]

  render () {
    return (
      <div className="card">
        <div className="card-block">
          <table>
            <thead>
            <tr>
              <th colSpan="4">Authority Handover Form</th>
            </tr>
            </thead>
            <tbody>
              <tr>
                
              </tr>
            </tbody>
          </table>
          <form>
              <div className="col-sm-6 col-md-3">
                <Field name="type" component={renderReactSelectWrapper}
                       options={this.authority_handover_type}
                       label="Handover Type"
                />
              </div>
              <div className="col-sm-6 col-md-3">
                <Field name="parent" component={renderReactSelectWrapper}
                       options={getOptions('authority_handover', 'authority_handover', '/api/v1/authority-handover/choices/')}
                       label="Parent Handover"
                />
              </div>
              <div className="col-sm-6 col-md-3">
                <Field name="beneficiary" component={renderReactSelectWrapper}
                       options={getOptions('authority_handover', 'beneficiary', '/api/v1/beneficiary/choices/')}
                       label="Beneficiary Office"
                />
              </div>
              <div className="col-sm-6 col-md-3">
                <Field name="fiscal_year" component={renderReactSelectWrapper}
                       options={getOptions('core', 'fiscal_year', '/api/v1/fiscal-year/choices/')}
                       label="Fiscal Year"
                />
              </div>
              <div className="col-sm-6 col-md-3">
                <Field name="budget_head" component={renderReactSelectWrapper}
                       options={getOptions('core', 'budget_head', '/api/v1/budget-head/choices/')}
                       label="Budget Head"
                />
              </div>
              <div className="col-sm-6 col-md-3">
                <Field name="priority_code" type="text" label="Priority" component={renderField}/>
              </div>
              <div className="col-sm-6 col-md-3">
                <Field name="date" type="date" label="Date" component={renderField}/>
              </div>
            </div>
            <div>
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
  form: 'authority_handover'
})(AuthorityHandoverForm)

export default AuthorityHandover