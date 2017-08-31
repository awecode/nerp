import React from 'react'
import { Field, FieldArray } from 'redux-form'
import { renderField, renderReactSelectWrapper } from '../../../project/utils/ReduxFormFieldComponents'

export class ForeignFundForm extends React.Component {

  render = () => {
    // debugger;
    return (
      <div>
        <button type="button" onClick={() => this.props.fields.push({})}>
          Add Foreign Fund
        </button>
        {this.props.meta.error && <span>{this.props.meta.error}</span>}
        {this.props.fields.map(
          (budget_distribution, index) =>
            <div className="row" key={index}>
              <div className="col-sm-6 col-md-3">
                <Field name={`${budget_distribution}.budget_head`} component={renderReactSelectWrapper}
                       label="Budget Head"
                />
              </div>
              <div className="col-sm-6 col-md-3">
                <Field name={`${budget_distribution}.permitted_budget`} component={renderField}
                       label="Permitted Budget"
                       type="number"
                />
              </div>
              <div className="col-sm-6 col-md-3">
                <Field name={`${budget_distribution}.government_fund`} component={renderField}
                       label="Government Fund"
                       type="number"
                />
              </div>
              <div className="col-sm-6 col-md-3">
                <Field name={`${budget_distribution}.remarks`} component={renderField}
                       label="Remarks"
                       type="text"
                />
              </div>
              <div className="col-lg-4 col-md-6 col-sm-12">
                  <FieldArray name="foreign_funds" component={renderForeignFundForm} />
              </div>
              <div className="col-sm-6 col-md-3">
                <button
                  type="button"
                  title="Remove Distribution"
                  onClick={() => this.props.fields.remove(index)}
                >Remove Distribution
                </button>
              </div>

            </div>
        )}
      </div>
    )
  }
}

export const renderForeignFundForm = props => (<ForeignFundForm {...props}/>)