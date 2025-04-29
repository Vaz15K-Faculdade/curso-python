import pandas as pd

df = pd.read_csv('Aula 25-04-22/Ecommerce_Consumer_Behavior_Analysis_Data.csv')

df_fem = df[df["Gender"] == 'Female']
df_masc = df[df["Gender"] == 'Male']

# Perguntas:

# Qual é o público alvo?
#Customer_ID,Age,Gender,Income_Level,Marital_Status,Education_Level,Occupation,Location,Purchase_Category,Purchase_Amount,Frequency_of_Purchase,Purchase_Channel,Brand_Loyalty,Product_Rating,Time_Spent_on_Product_Research(hours),Social_Media_Influence,Discount_Sensitivity,Return_Rate,Customer_Satisfaction,Engagement_with_Ads,Device_Used_for_Shopping,Payment_Method,Time_of_Purchase,Discount_Used,Customer_Loyalty_Program_Member,Purchase_Intent,Shipping_Preference,Time_to_Decision

# quantidade de cada gênero
print(df["Gender"].value_counts())

# porcentagem de cada gênero
print(df["Gender"].value_counts(normalize=True) * 100)

# Quantos solteiros tem?
print(f"Numero de Solteiros: {df['Marital_Status'].value_counts()['Single']}")

# Qual é a idade média dos clientes?

# Qual é a idade média por nível de renda?

# Qual é a idade média por gênero?

# Qual é a proporção de clientes por nível de renda (Baixa, Média, Alta)?

# print(proporcao_nivel_renda.map(lambda x: f'{x:.2f}%'))

# print(f'proporção de clientes por nível de renda (Baixa, Média, Alta): {df['Income_Level'].value_counts(normalize=True) * 100}')

# Qual é a categoria de produto mais comprada?

# Qual é o valor médio gasto por compra?

# Qual é o método de pagamento mais usado?

# Quantas compras foram feitas online vs. em loja física?

# Qual é a avaliação média dos produtos?

# O valor médio de compra é maior para clientes do gênero feminino ou masculino?

# O valor médio de compra pelo marital status

