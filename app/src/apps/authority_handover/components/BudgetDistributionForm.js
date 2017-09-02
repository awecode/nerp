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
            <div className="card bg-faded" key={index}>
              <div className="card-block">
                <div className="row">
                  <div className="col-6">
                    <table className="table table-striped input-table table-bordered">
                      <thead>
                      <tr>
                        <th colSpan="2">Budget Distribution #{index+1}</th>
                      </tr>
                      </thead>
                      <tbody>
                      <tr>
                        <td>Expenditure Head</td>
                        <td>
                          <Field name={`${budget_distribution}.expenditure_head`} component={renderReactSelectWrapper}
                                 label="Expenditure Head"
                                 options={getOptions('authority_handover', 'expenditure_head', '/api/v1/expenditure-head/choices/')}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td>Permitted Budget</td>
                        <td>
                          <Field name={`${budget_distribution}.permitted_budget`} component={renderField}
                                 label="Permitted Budget"
                                 type="number"
                          />
                        </td>
                      </tr>
                      <tr>
                        <td>Government Fund</td>
                        <td>
                          <Field name={`${budget_distribution}.government_fund`} component={renderField}
                                 label='Government Fund'
                                 type='number'
                          />
                        </td>
                      </tr>
                      <tr>
                        <td>Remarks</td>
                        <td>
                          <Field name={`${budget_distribution}.remarks`} component={renderField}
                                 label="Remarks"
                                 type="text"
                          />
                        </td>
                      </tr>
                      </tbody>
                    </table>
                    <button
                      className='btn btn-danger'
                      type='button'
                      title='Remove Distribution'
                      onClick={() => this.props.fields.remove(index)}
                    >Remove Budget Distribution # {index + 1}
                    </button>
                  </div>
                  <div className="col-6">
                    <FieldArray name={`${budget_distribution}.foreign_funds`} component={renderForeignFundForm}/>
                  </div>
                </div>
              </div>
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