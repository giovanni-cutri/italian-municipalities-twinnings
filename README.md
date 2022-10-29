![Socialify](https://github.com/giovanni-cutri/italian-municipalities-twinnings/blob/main/resources/socialify-logo.png)

# italian-municipalities-twinnings
 
This Python script scrapes data from the Italian Wikipedia to get a list of all the twinnings of the Italian municipalities between them and the rest of the world.

Data is stored in two CSV files:
- **twinnings.csv** is used for municipalities that have at least one twinning and contains the following information:
    - **country**, **region**, **province** and **name** of the municipality *(note that "country" field is always Italy)*
    - **country** and **name** of the twinned municipality *(which can be Italian or foreign)*
- **twinningless.csv** is used for municipalities that do not currently have any twinnings: it simply stores their country, region, province and name.

An example of SQL query is also available: it sorts the municipalities by twinnings count in descending order.

## Dependencies

All the necessary libraries are listed in the *requirements.txt* file.

You can install them by running:

```
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/giovanni-cutri/italian-disney-comics-covers/blob/main/LICENSE) file for details.
