# hotel-price-visualisation
You can access the app here: https://hotel-price-visualisation.onrender.com/

Note: The app may take a few minutes to load and will be slower as it is hosted on a free-tier service.
If the app does not load (it may go to sleep after a period of inactivity), feel free to email me and I will restart it.

## Demo
Watch the demo here:
[https://youtu.be/o_I8Ru9TS58](https://youtu.be/o_I8Ru9TS58)

## 1. Visualisation Modes
Two visualisation mode:
### Linear Mode
Plots selected years one after the other for side-by-side comparison.

### Overlapping Mode
Plots selected years on the same timeline to easily compare patterns.

## 2. Period Selection
Helps with visually identifying middle of year, year quarters etc.

## 3. Month-Based
Used to zoom into specific months to focus on shorter time frames.
Note:
- Since 2012 includes February 29, there is a natural break for other years when aligning dates.
- Also noticed missing data for the date 7/13/2012

## 4. Outlier Visualisation
Dashboard includes a scatter plot view to highlight potential outliers.
- One clearly visible example is 03/12/2015
- Outliers are marked separately

You can enable or disable outlier visualisation using the toggle switch.

## 5. Adjustable IQR Multiplier
For outlier detection, I decided to go with IQR
- Default multiplier: 1.5
- You can adjust the multiplier using the slider
- Increasing the multiplier makes detection less sensitive
- Decreasing the multiplier makes detection more sensitive

**NOTE**
Outliers are calculated dynamically based on your selection:
- If you select a single year -> outliers are calculated using only that year's data
- If you select specific months -> calculation uses only those months
- If you select multiple years -> calculation uses data from those selected years

Some points marked as outliers may represent price spikes rather than true anomalies.
If I consider the data to be for short term rentals, they may represent holidays, festivals or peak season.
So, these should be interpreted carefully.
