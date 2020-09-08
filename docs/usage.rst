=====
Usage
=====

To use finance_calculator in a project::

	import finance_calculator

You can use finance calculator with pandas or you can just pass
the required data in specified formats and get the calculated data.

Let's say we have a pandas dataframe df which contains date and nav with date as index.

.. code-block:: python

    new_df_with_treynor = finance_calculator.get_treynor(df)
    new_df_with_beta = finance_calculator.get_beta(df)
    new_df_with_alpha = finance_calculator.get_alpha(df)


Else if you have data as a list of tuple: [(date, nav)]

.. code-block:: python

    date_treynor_tuple_list = finance_calculator.get_treynor(date_nav_tuple_list)
