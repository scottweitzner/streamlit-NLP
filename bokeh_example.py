"""
NLP use cases for streamlit. this was forked from Mark Marc Skov Madsen's reop here:
https://github.com/MarcSkovMadsen/awesome-streamlit/tree/master/gallery/bokeh_experiments

NLTK
nltk.download('tagsets')
"""

import bokeh
import bokeh.layouts
import bokeh.models
import bokeh.plotting
import markdown
import pandas as pd
import streamlit as st

import nltk
from nltk import word_tokenize


def main():
    tabs = bokeh.models.Tabs(
        tabs=[
            sentiment_tagging_panel(),
            pos_tagging_panel()
        ],
        sizing_mode='stretch_width'
    )
    st.bokeh_chart(tabs)

    print(nltk.help.upenn_tagset())


def pos_tagging_panel():
    text = word_tokenize("And now for something completely different")
    nltk.pos_tag(text)


def sentiment_tagging_panel():

    st.markdown("""
#### This is an example of using streamlit + bokeh to produce tagging on text
In this case the tagging is sentiment tags from a kaggle dataset 
[here](https://www.kaggle.com/c/tweet-sentiment-extraction/data). Click on a row to see it in action.
    """)

    sentiment_df = pd.read_csv('sentiment_train.csv')
    source = bokeh.models.ColumnDataSource(sentiment_df)

    columns = [
        bokeh.models.widgets.TableColumn(field="text", title="Text"),
        bokeh.models.widgets.TableColumn(field="selected_text", title="Selected Text"),
        bokeh.models.widgets.TableColumn(field="sentiment", title="Sentiment"),
    ]
    data_table = bokeh.models.widgets.DataTable(source=source, columns=columns, height=500, sizing_mode="stretch_width")

    text = """
    """
    text_div = bokeh.models.widgets.markups.Div(text=markdown.markdown(text), sizing_mode="stretch_width")
    callback = bokeh.models.CustomJS(
        args=dict(table=source, text_div=text_div),
        code="""
        
var selected_rows = table.selected.indices;
var text = table.data.text[selected_rows];
var sentiment_text = table.data.selected_text[selected_rows];
var sentiment = table.data.sentiment[selected_rows];

var color = sentiment == 'negative' ? '#FFA2A2' : sentiment === 'positive' ? '#96E6A8' : '#FFFD7A';
var replaced = `<span style="background-color:${color}">&nbsp${sentiment_text}&nbsp</span>`;
text = text.replace(sentiment_text, replaced)
text_div.text = `<br>${text}`;
text_div.change.emit();
        """,
    )
    source.selected.js_on_change('indices', callback)
    column = bokeh.layouts.Column(children=[text_div, data_table], sizing_mode="stretch_width")

    return bokeh.models.Panel(child=column, title="Sentiment Tagging")


if __name__ == '__main__':
    main()
