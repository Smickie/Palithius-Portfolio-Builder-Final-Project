# Palithius-Portfolio-Builder-Final-Project
 
Hello! Welcome to this github repository of my final project during my studies at Nod Coding Bootcamp. 

In this final project, we truly put our autonomous coding to the test by branching out to new libraries and trying new things. In my case, I created a streamlit enviorment where one can screen and quickly get overviews of different nordic listed companies fundamentals with options to add said company to your portfolio. 

The analysis screen comprises of company description, industry and branch, positive & negative macro-signals for said branch. It contains a historical overview of the shareprice and fundamental data from the company's last 10 quarterly reports. Finally, it can compare simple valuation metrics such as P/E, P/FCF & P/B scores to where the company is currently valued according to these metrics and how it compares to other companies in the same branch (a bit computionally heavy...) 

The portfolio optimizer is an easy to use interface that allows the user to fully customize their portfolio with complimentary statistics such as expected returns, risk, sharpe ratio and value at risk. It shows historical returns of the portfolio as well as simulated returns when assuming returns to be normally distributed.

Using skfolios machine learning library we also help the user in fully realizing the potential of their portfolio by automatically maximizing the ratio between expected return and risk where the user can customize minimum/maximum weights in assets and time horizons to their liking. 

## Libraries used:

Seaborn
Matplotlib
Streamlit
Yahoo Finance
Skfolio
Pandas
Numpy
... And some others.

## APIs:

Börsdata API - Pro Key required to run. 

## About the files

main1 includes only the share overview function.
main2 is the finished project with the portfolio builder included. 

This can either be run in a command prompt or in a jupyter notebook (which i did in the streamlit runner notebook) 

The playground notebooks is for learning the different libraries and APIs that I used, börsdata was quite difficult to nail down at first but once you understood how to use requests to get data you wanted it became much easier thanks to the swagger documentation. 

Translation & Macro .py files are simple mapping tools we used in our enviorment. Macro for the flags in the overview section and translation to make the choice of fundamental data more natural in the program.