import React from 'react'
import { Field, FieldArray } from 'redux-form'
import { renderField, renderReactSelectWrapper } from '../../../project/components/ReduxFormFieldComponents'
import { renderForeignFundForm } from './ForeignFundDetailForm'
import { getOptions } from '../../server_data/actions/query'

class BudgetDistributionForm extends React.Component {

  render = () => {
    return (
      <div>
        {this.props.meta.error && <span>{this.props.meta.error}</span>}
        {this.props.fields.map(
          (budget_distribution, index) =>
            <div key={index}>
              <table className="table table-striped input-table table-bordered">
                <thead>
                <tr>
                  <th>Expenditure Head</th>
                  <th>Permitted Budget</th>
                  <th>Government Fund</th>
                  <th>Remarks</th>
                  <th></th>
                </tr>
                </thead>
                <tbody>
                <tr>
                  <td>
                    <Field name={`${budget_distribution}.expenditure_head`} component={renderReactSelectWrapper}
                           label="Expenditure Head"
                           options={getOptions('authority_handover', 'expenditure_head', '/api/v1/expenditure-head/choices/')}
                    />
                  </td>
                  <td>
                    <Field name={`${budget_distribution}.permitted_budget`} component={renderField}
                           label="Permitted Budget"
                           type="number"
                    />
                  </td>
                  <td>
                    <Field name={`${budget_distribution}.government_fund`} component={renderField}
                           label='Government Fund'
                           type='number'
                    />
                  </td>
                  <td>
                    <Field name={`${budget_distribution}.remarks`} component={renderField}
                           label="Remarks"
                           type="text"
                    />
                  </td>
                  <td>
                    <button
                      className='btn btn-danger'
                      type='button'
                      title='Remove Distribution'
                      onClick={() => this.props.fields.remove(index)}
                    >Remove Budget Distribution
                    </button>
                  </td>
                </tr>
                </tbody>
              </table>
              <FieldArray name={`${budget_distribution}.foreign_funds`} component={renderForeignFundForm}/>
            </div>
        )}
        <button type="button" onClick={() => this.props.fields.push({})} className="btn btn-success">
          Add Budget Distribution
        </button>

      </div>
    )
  }
}

export const renderBudgetDistributions = props => (<BudgetDistributionForm {...props}/>)