/*
Author: Jake Bernard
Date: Nov 24, 2024
File: Chart.jsx
Purpose: Chart component for displaying user's financial data
Input:
- period:
  - the period in days you want to show back for expenses. passing in null (or leaving this blank) shows from the first expense.
- budget:
  - the budget information. not yet used.
- expenses:
  - array of expense objects
- income:
  - array of income objects. NB: can't display them on the chart properly because they have no associated date. And I didn't make time to implement recurring income.
- width:
  - number. determines width of whole thing. somewhere around window.innerWidth / 2 or / 3 might work best.
- height
  - number. same thing. window.innerHeight /2 or /3, maybe for recommended value
- animation:
  - bool to toggle animations. unused.
*/

import React from "react";
import Chart from 'chart.js/auto';
import {Bar, Doughnut, Line} from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';



function ExpenseChart({ period, budget, expenses, income, width, height, animation }) {

  let dateLimit = null;
  if (period) {
    dateLimit = new Date();
    dateLimit.setTime( dateLimit.getTime() - period * 86400000 );
  }

  function Color(r, g, b) {
    this.r = r;
    this.g = g;
    this.b = b;
    this.clone = function() {
      return new Color(this.r, this.g, this.b);
    }
    this.asString = function () {
      return `rgb(${Math.floor(r)},${Math.floor(g)},${Math.floor(b)})`;
    }
    this.add = function(other) {
      return new Color(other.r + this.r, other.g + this.g, other.b + this.b);
    }
    this.mult = function(scalar) {
      return new Color(scalar * this.r, scalar * this.g, scalar * this.b);
    }
    this.makeInterpolator = function(other, div)  {
      let diff = this.add(other.mult(-1));
      return diff.mult(1/div);
    }
  }

  function makeLinearPalette(start, end, shades) {
    let interp = end.makeInterpolator(start, Math.max(shades - 1, 1));
    const palette = [];
    let current = start.clone();
    for (let i = 0; i < shades; i++) {
      palette.push(current);
      current = current.add(interp);
    }
    return palette;
  }

  let expenseStartColor = new Color(255, 91, 56);
  let expenseEndColor = new Color(139,  0, 110);
  let expensePalette = [];

  let incomeStartColor = new Color(151, 255, 43);
  let incomeEndColor = new Color(18, 212, 2);
  let incomePalette = [];

  const timelineSize = {width: width * 0.65, height: height};
  const tinyChartSize = {width: width, height: height};

  let expensesCategorized = {};
  let incomeCategorized = {};
  let budgetCategorized = {};

  let expenseChartData;
  let incomeChartData;
  let timelineChartData;

  if (expenses || income) {
    if (expenses) {
      expenses.forEach( expense =>
        {
          if (period) {
            if (expense.date < dateLimit) {
              return;
            }
          }

          if (!expensesCategorized[expense.category]) {
            expensesCategorized[expense.category] = [{x: expense.date, y: expense.amount}];
          }
          else {
            expensesCategorized[expense.category].push({x: expense.date, y: expense.amount});
          }
        }
      );
      expensePalette = makeLinearPalette(expenseStartColor, expenseEndColor, Object.keys(expensesCategorized).length);          

      expenseChartData = {
          type: "doughnut",
          labels: Object.keys(expensesCategorized),
          datasets: [{
            label: "Expenses by Category",
            data: (() => {
              let dataOut = [];
              for (let i = 0; i < Object.keys(expensesCategorized).length; i++) {
                dataOut.push(
                  expensesCategorized[Object.keys(expensesCategorized)[i]].reduce(
                    (acc, cur) => acc + cur.y,
                    0
                  )
                );
              }
              return dataOut;
            })(),
          backgroundColor: (() => {
            let colorsOut = [];
            expensePalette.forEach((value) => colorsOut.push(value.asString()));
            return colorsOut;
          })()
        }]
        };

    }

    if (income) {
      income.forEach( inc =>
        {
          if (period) {
            if (income.date < dateLimit) {
              return;
            }
          }

          if (!incomeCategorized[inc.source_name]) {
            incomeCategorized[inc.source_name] = [{x: inc.date, y: inc.amount}];
          }
          else {
            incomeCategorized[inc.source_name].push({x: inc.date, y: inc.amount});
          }
        }
      );
      incomePalette = makeLinearPalette(incomeStartColor, incomeEndColor, Object.keys(incomeCategorized).length);
    
      incomeChartData = {
          labels: Object.keys(incomeCategorized),
          type: "doughnut",
          datasets: [{
            label: "Income by Category",
            data: (() => {
              let dataOut = [];
              for (let i = 0; i < Object.keys(incomeCategorized).length; i++) {
                dataOut.push(
                  incomeCategorized[Object.keys(incomeCategorized)[i]].reduce(
                    (acc, cur) => acc + cur.y,
                    0
                  )
                );
              }
              return dataOut;
            })(),
          backgroundColor: (() => {
            let colorsOut = [];
            incomePalette.forEach((value) => colorsOut.push(value.asString()));
            return colorsOut;
          })()
        }]
        };
    }

  timelineChartData = {
        type: "bar",
        datasets: (() => {
          let datasetsOut = [];
          for (let i = 0; i < Object.keys(expensesCategorized).length; i++) {
            let dataset = {};
            dataset.active = true;
            dataset.data = expensesCategorized[Object.keys(expensesCategorized)[i]];
            dataset.backgroundColor = expensePalette[i].asString();
            dataset.borderWidth = 0;
            dataset.label = Object.keys(expensesCategorized)[i];
            datasetsOut.push(dataset);
          }
          // for (let i = 0; i < Object.keys(incomeCategorized).length; i++) {
          //   console.log(incomeCategorized);
          //   let dataset = {};
          //   dataset.data = incomeCategorized[Object.keys(incomeCategorized)[i]];
          //   dataset.backgroundColor = incomePalette[i];
          //   dataset.label = Object.keys(incomeCategorized)[i];
          //   datasetsOut.push(dataset);
          // }
          return datasetsOut;
        })()
      };
  }
  
console.log(timelineChartData);

  return (
    <div style={{ backgroundColor: "var(--white)",
                  display: "flex",
                  flexDirection: "column",
                  height: height + "px",
                  width: width + "px"
     }}
    id="chartContainer">
      <div style={{ height: height / 2 + "px", display: "flex", justifyContent: "center"}}>
        {expenses ? 
        (<Bar id="timeline-chart" 
             data={timelineChartData}
             options={
              {plugins: {legend: {display: false}}, 
               scales: {
              x: {
                  type: 'time',
                  bounds: "data"
              }
            }}
            }
             height={height + "px"}
             width={width + "px"}
             style={{backgroundColor : "var(--white)"}}/>)
        :
        (<></>)
        }
      </div>
      <div style={{
                    display: "flex",
                    height: height / 2 + "px",
                    justifyContent: "space-evenly"}}>
          {income ?
          (<Doughnut id="income-pie-chart" 
             data={incomeChartData}
             style={{backgroundColor : "var(--white)"}}/>)
             : (<></>)}
          {expenses ?   
          (<Doughnut id="expense-pie-chart" 
             data={expenseChartData}
             style={{backgroundColor : "var(--white)",}}/>)
             : (<></>)}

      </div>
    </div>
  );
}

export default ExpenseChart;

