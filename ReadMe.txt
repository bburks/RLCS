In this project, we create a model to predict the outcome of rocket league matches.

The full scope:

-Pull RLCS data from Octane.gg and save it to a Pandas dataframe (CSV file).
  -Keep track of the date, and make new api requests for data.
-Evaluate match data to track a TrueSkill rating for each team.
  -Implement this region by region, normalizing region ratings through Major data.
  -Store ratings (up to a date) in a Pandas dataframe
-Build a framework to simulate RLCS events. Each is an iterator of games to
  complete, where the seeding of the next game depends on prior results.
