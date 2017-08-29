import React from 'react'
import { Field, reduxForm } from 'redux-form'
import { renderReactSelectWrapper } from '../../../project/utils/ReduxFormSelect'

// todo translation

class BudgetDistributionForm extends React.Component {
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
        </div>
        <div className="row">
          <div>

          </div>
        </div>
      </form>
    )
  }
}

const BudgetDistribution = reduxForm({
  // a unique name for the form
  form: 'budget_distribution'
})(BudgetDistributionForm)

export default BudgetDistribution