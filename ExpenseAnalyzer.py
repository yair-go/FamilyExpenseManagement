import pandas as pd
from time import strftime
import os 


category_options = list(pd.read_csv('category_options.csv'))


def enter_categories_from_user():
    input('Do you want to reset the list of categories ?')


def choose_category(b):
    for i, option in enumerate(category_options):
        print(i, option)
    choice = int(input(b[::-1] + " : " ))
    return category_options[choice]
        

# Data preparation
def get_categories(credit_expenses):
    business = credit_expenses['Business'].unique()
    categories = pd.read_csv('Categories.csv')
    
    new_business = [b for b in business if b not in list(categories['business'])]
    
    d = {}
    for b in new_business:
       category = choose_category(b)
       d[b] = category
    
    new_categories = pd.DataFrame(d.items(), columns=['business', 'category'])
    categories = pd.concat([categories, new_categories], ignore_index = True) 
    
    categories.to_csv('Categories.csv', index=False, encoding = 'utf-8-sig')
    return categories
    

def main():
    if len(category_options) == 2:
        enter_categories_from_user()
    df = pd.DataFrame(columns = category_options)
    
    filename = input("insert file name : ")
    credit_expenses = pd.read_csv(filename + '.csv')
    the_current_month = strftime('%m_%y')
    
    if not os.path.exists(the_current_month): 
        os.makedirs(the_current_month) 
    
   # Analyzing the data

    categories = get_categories(credit_expenses)

    for i, row in credit_expenses.iterrows():
        category = categories[categories['business'] == row['Business']]['category'].values[0]
        credit_expenses.loc[i, 'Category'] = category

    credit_expenses.to_csv(the_current_month + '/' + filename + '_new.csv', index=False, encoding = 'utf-8-sig')

    for i, row in credit_expenses.iterrows():
        category = row['Category']
        df.loc[i, category] = row['Debit']

    df = df.apply(lambda x: x.sort_values().values)
    df = df.dropna(how='all')

    df.to_csv(the_current_month + '/' +'Credit_expenses_By_Category_' + the_current_month + '.csv')

    fixed = credit_expenses[credit_expenses['Category'] == 'Fixed']
    fixed = fixed.drop(columns=['Transaction'])
    fixed.to_csv(the_current_month + '/' +'Fixed_' + the_current_month + '.csv', index=False, encoding = 'utf-8-sig')
    unknown = credit_expenses[credit_expenses['Category'] == 'Unknown']
    unknown = unknown.drop(columns=['Transaction'])
    unknown.to_csv(the_current_month + '/' +'Unknown_' + the_current_month + '.csv', index=False, encoding = 'utf-8-sig')
    
    with pd.ExcelWriter(the_current_month + '/' + 'summary.xlsx') as writer:
        credit_expenses.to_excel(writer, sheet_name='credit_expenses')
        df.to_excel(writer, sheet_name='By_Category')
        fixed.to_excel(writer, sheet_name='fixed')
        unknown.to_excel(writer, sheet_name='unknown')
    

if __name__ == "__main__":
    main()
