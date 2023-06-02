from flask import Flask,render_template, request
import pickle as pk

import numpy as np



application = Flask("__name__")

book_data = pk.load(open('TopBook.pkl', 'rb'))

filter_books = pk.load(open('filtered_Books.pkl','rb'))

similar_books = pk.load(open('similar_Books_Score.pkl','rb'))

p_table = pk.load(open('p_Table.pkl','rb'))



@application.route('/')
def index():
    return render_template('index.html',
                           book_name = list(book_data['Book-Title'].values),
                           book_image = list(book_data['Image-URL-M'].values),
                           book_author = list(book_data['Book-Author'].values),
                           book_rating = list(book_data['Rating'].values)
                            )

@application.route('/recommend')
def recommend_book():
    return render_template('recommend.html')

@application.route('/recommend_books',methods=['post'])
def recom():
    user_input = request.form.get('user_input')
    if user_input in filter_books['Book-Title'].values:
        index = np.where(p_table.index == user_input)[0][0]
        Books_List = sorted(list(enumerate(similar_books[index])), key = lambda x:x[1], reverse = True)[1:6]
        
        required_data = []
        for x in Books_List:
            information = []    
            temp_df = filter_books[filter_books['Book-Title'] == p_table.index[x[0]]]
            information.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            information.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            information.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            required_data.append(information)

        # print(required_data)
        return render_template('recommend.html', data=required_data)
    else:
        return render_template('recommend.html',data = [])


# if __name__ == "__main__":
#     app.run(debug=True)