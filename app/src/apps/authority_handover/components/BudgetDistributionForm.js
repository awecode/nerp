import React from 'react'
import { Field, FieldArray } from 'redux-form'
import { renderField, renderReactSelectWrapper } from '../../../project/components/ReduxFormFieldComponents'
import { renderForeignFundForm } from './ForeignFundDetailForm'

class BudgetDistributionForm extends React.Component {

  render = () => {
    return (
      <div>
        <div className="col-12">
          <button type="button" onClick={() => this.props.fields.push({})} className="btn btn-success">
            Add Budget Distribution
          </button>
        </div>

        {this.props.meta.error && <span>{this.props.meta.error}</span>}
        {this.props.fields.map(
          (budget_distribution, index) =>
            <div className="card">
              <div className="card-block bg-gray">
                <div className="row" key={index}>
                  <div className="col-sm-6 col-md-3">
                    <Field name={`${budget_distribution}.expenditure_head`} component={renderReactSelectWrapper}
                           label="Expenditure Head"
                    />
                  </div>
                  <div className="col-sm-6 col-md-2">
                    <Field name={`${budget_distribution}.permitted_budget`} component={renderField}
                           label="Permitted Budget"
                           type="number"
                    />
                  </div>
                  <div className="col-sm-6 col-md-2">
                    <Field name={`${budget_distribution}.government_fund`} component={renderField}
                           label="Government Fund"
                           type="number"
                    />
                  </div>
                  <div className="col-sm-6 col-md-2">
                    <Field name={`${budget_distribution}.remarks`} component={renderField}
                           label="Remarks"
                           type="text"
                    />

                  </div>
                  <div className="col-sm-6 col-md-3">
                    <button
                      className="btn btn-danger"
                      type="button"
                      title="Remove Distribution"
                      onClick={() => this.props.fields.remove(index)}
                    >Remove Budget Distribution
                    </button>

                  </div>
                  <div className="col-12">
                    <FieldArray name="foreign_funds" component={renderForeignFundForm}/>
                  </div>
                </div>
              </div>
            </div>
        )}
      </div>
    )
  }
}

export const renderBudgetDistributions = props => (<BudgetDistributionForm {...props}/>)