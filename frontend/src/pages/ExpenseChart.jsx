/*
Author: Jake Bernard
Date: Nov 24, 2024
File: Chart.jsx
Purpose: Chart component for displaying user's financial data
*/

import React, { useRef, useEffect } from "react";
import { Chart } from 'chart.js';

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
    let interp = start.makeInterpolator(end, Math.max(shades - 1, 1));
    const palette = [];
    let current = start.clone();
    for (let i = 0; i < shades; i++) {
      palette.push(current);
      current = current.add(interp);
    }
    return palette;
  }

  let expenseStartColor = new Color(255, 91, 56);
  let expenseEndColor = new Color(189,  9, 90);
  let expensePalette = [];

  let incomeStartColor = new Color(151, 255, 43);
  let incomeEndColor = new Color(18, 212, 2);
  let incomePalette = [];

  const timelineChart = useRef(null);
  const incomePie     = useRef(null);
  const expensePie    = useRef(null);
  const budgetBar     = useRef(null);

  const timelineSize = {width: width * 0.65, height: height};
  const tinyChartSize = {width: width * 0.35, height: height * 0.333};

  useEffect(() => {
      timelineChart.current.width = timelineSize.width + "px";
      timelineChart.current.height = timelineSize.height + "px";
      timelineChart.current.backgroundColor = "var(--white)";
      const timelineCtx = timelineChart.current.getContext("2d");
      
      incomePie.current.width = tinyChartSize.width + "px";  
      incomePie.current.height = tinyChartSize.height + "px";
      incomePie.current.backgroundColor = "var(--white)";
      const incomeCtx = incomePie.current.getContext("2d");

      expensePie.current.width = tinyChartSize.width + "px";  
      expensePie.current.height = tinyChartSize.height + "px";
      expensePie.current.backgroundColor = "var(--white)";
      const expenseCtx = expensePie.current.getContext("2d");

      budgetBar.current.width = tinyChartSize.width + "px";  
      budgetBar.current.height = tinyChartSize.height + "px";
      budgetBar.current.backgroundColor = "var(--white)";
      const budgetCtx = budgetBar.current.getContext("2d");

      const expensesCategorized = {};
      const incomeCategorized = {};
      const budgetCategorized = {};

      let expenseChart;
      let incomeChart;
      let timelineChartChart;

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
          

          expenseChart = new Chart(expenseCtx, {
            data: {
              type: "doughnut",
              labels: Object.keys(expensesCategorized),
              datasets: [{
                label: "Expenses by Category",
                data: (() => {
                  let dataOut = [];
                  for (let i = 0; i < Object.keys(expensesCategorized).length; i++) {
                    dataOut.push(
                      expensesCategorized[Object.keys(expensesCategorized)[i]].reduce(
                        (acc, cur) => acc.x + cur,
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
            }
          });

        }

        if (income) {
          income.forEach( inc =>
            {
              if (period) {
                if (income.date < dateLimit) {
                  return;
                }
              }

              if (!incomeCategorized[inc.category]) {
                incomeCategorized[inc.category] = [{x: inc.date, y: inc.amount}];
              }
              else {
                incomeCategorized[inc.category].push({x: inc.date, y: inc.amount});
              }
            }
          );
          incomePalette = makeLinearPalette(incomeStartColor, incomeEndColor, len(Object.keys(incomeCategorized)));
        
          incomeChart = new Chart(incomeCtx, {
            data: {
              labels: Object.keys(incomeCategorized),
              type: "doughnut",
              datasets: [{
                label: "Income by Category",
                data: (() => {
                  let dataOut = [];
                  for (let i = 0; i < Object.keys(incomeCategorized).length; i++) {
                    dataOut.push(
                      incomeCategorized[Object.keys(incomeCategorized)[i]].reduce(
                        (acc, cur) => acc.x + cur,
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
            }
          });

        
        }

      timelineChartChart = new Chart(timelineCtx, {
          data: {
            type: "bar",
            datasets: (() => {
              let datasetsOut = [];
              for (let i = 0; i < Object.keys(expensesCategorized).length; i++) {
                let dataset = {};
                dataset.data = expensesCategorized[Object.keys(expensesCategorized)[i]];
                dataset.backgroundColor = expensePalette[i];
                dataset.label = Object.keys(expensesCategorized)[i];
                datasetsOut.push(dataset);
              }
              for (let i = 0; i < Object.keys(incomeCategorized).length; i++) {
                let dataset = {};
                dataset.data = incomeCategorized[Object.keys(incomeCategorized)[i]];
                dataset.backgroundColor = expensePalette[i];
                dataset.label = Object.keys(incomeCategorized)[i];
                datasetsOut.push(dataset);
              }
            })()
          }
      });
      
      }

      return () => {
        expenseChart.destroy();
        incomeChart.destroy();
        timelineChartChart.destroy();
      }
    }, 
  []);



  return (
    <div style={{ backgroundColor: "var(--white)",
                  width: "100%",
                  height: "100%"
    }}
    id="chartContainer">
      <div style={{ float: "left", 
                    width: "65%" }}>
        <canvas id="timeline-chart" ref={timelineChart}></canvas>
      </div>
      <div style={{ float: "right",
                    width: "35%"  }}>
        <div style={{ display: "flex",
                      flexDirection: "column" }}>
          <canvas id="income-pie-chart" ref={incomePie}></canvas>
          <canvas id="expense-pie-chart" ref={expensePie}></canvas>
          <canvas id="budget-bar-chart" ref={budgetBar}></canvas>
        </div>

      </div>
    </div>
  );
}

export default ExpenseChart;

