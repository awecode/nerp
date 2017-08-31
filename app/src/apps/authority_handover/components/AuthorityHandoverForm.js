import React from 'react'
import { Field, FieldArray, reduxForm } from 'redux-form'
import { renderField, renderReactSelectWrapper } from '../../../project/utils/ReduxFormFieldComponents'
import { renderBudgetDistributions } from './BudgetDistributionForm'

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
      <form>
        <div className="row">
          <div className="col-sm-6 col-md-3">
            <Field name="type" component={renderReactSelectWrapper}
                   options={this.authority_handover_type}
                   label="Handover Type"
            />
          </div>
          <div className="col-sm-6 col-md-3">
            <Field name="parent" component={renderReactSelectWrapper}
                   options={this.props.parent_options}
                   label="Parent Handover"
            />
          </div>
          <div className="col-sm-6 col-md-3">
            <Field name="beneficiary" component={renderReactSelectWrapper}
                   options={this.props.beneficiary_options}
                   label="Beneficiary Office"
            />
          </div>
          <div className="col-sm-6 col-md-3">
            <Field name="fiscal_year" component={renderReactSelectWrapper}
                   options={this.props.fiscal_year_options}
                   label="Fiscal Year"
            />
          </div>
          <div className="col-sm-6 col-md-3">
            <Field name="budget_head" component={renderReactSelectWrapper}
                   options={this.props.budget_head_options}
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
          <FieldArray name="budget_distributions" component={renderBudgetDistributions} />
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