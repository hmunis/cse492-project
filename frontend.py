import sqlite3

import datetime
from datetime import datetime, timedelta

import plotly.graph_objects as go
from multidict import MultiDict

from backend import *
from utils import *


def main():
    # Set page config
    # At the start of your main() function
    st.set_page_config(
        page_title="Review Analyzer",
        page_icon="📱",
        layout="wide"
    )

    st.markdown("""
        <h1 style='text-align: center;'>
            Play Store Review Analyzer
        </h1>
        <p style='text-align: center; color: #666666;'>
        </p>
        """, unsafe_allow_html=True)

    # Connect to SQLite database
    conn = sqlite3.connect("C:/Users/hadic/PycharmProjects/ReviewAnalyzer/playstore_reviews_first.db")

    app_names = get_apps_names(conn)
    app_ids = get_apps_ids(conn)
    app_dict = dict(zip(app_names, app_ids))

    if 'can_generate_report' not in st.session_state:
        st.session_state.can_generate_report = False

    with st.sidebar:
        st.markdown("""
            <div style='text-align: center;'>
                <h2>⚙️ Settings</h2>
            </div>
            """, unsafe_allow_html=True)

        user_option = st.selectbox(
            label="Select an app",
            options=app_names,
            label_visibility="visible",
            placeholder="Choose an app..."
        )

        app_id = app_dict[user_option]

        st.image(
            get_header_img(app_id, conn),
            use_container_width=True
        )

        option_list = get_aspects(app_id, conn)
        option_list.insert(0, 'Select All')

        selected_options = st.multiselect(
            label = "Select aspect(s)",
            options=option_list,
            placeholder="Choose aspects to analyze"
        )

        if "Select All" in selected_options:
            selected_options = option_list[1:]  # Select all options except "Select All"
            st.success("You have selected the all aspects")
        else:
            if selected_options:
                st.success("You have selected the following aspects:")
                for aspect in selected_options:
                    st.write(f"- **{aspect}**")  # Display each selected value
            else:
                st.info("No aspects selected.")

        # get min and max dates from reviews in str format
        min_date = get_start_date(app_id, conn)
        max_date = get_end_date(app_id, conn)

        # convert str dates to datetime.date objects
        min_date = datetime.strptime(min_date, '%Y-%m-%d %H:%M:%S').date()
        max_date = datetime.strptime(max_date, '%Y-%m-%d %H:%M:%S').date()

        # generate list of all dates between min and max
        def generate_dates(start_date, end_date):
            date_list = []
            curr_date = start_date
            while curr_date <= end_date:
                date_list.append(curr_date)
                curr_date += timedelta(days=1)
            return date_list

        date_options = generate_dates(min_date, max_date)

        # Create date range slider
        selected_start_date, selected_end_date = st.select_slider(
            'Select date range',
            options=date_options,
            value=(min_date, max_date),
            format_func=lambda x: x.strftime('%Y-%m-%d')
        )

        number_of_opinion = st.radio(
            label="Select number of opinions",
            options=[1, 2, 3, 4, 5],
            help="Navigate to the Top Opinions tab to see mentions."
        )

    one_star_reviews = get_number_of_one_star_reviews(app_id, conn)
    two_star_reviews = get_number_of_two_star_reviews(app_id, conn)
    three_star_reviews = get_number_of_three_star_reviews(app_id, conn)
    four_star_reviews = get_number_of_four_star_reviews(app_id, conn)
    five_star_reviews = get_number_of_five_star_reviews(app_id, conn)
    review_numbers = [one_star_reviews, two_star_reviews, three_star_reviews, four_star_reviews, five_star_reviews]

    positive_sentences = get_number_of_positive_sentences(app_id, conn)
    negative_sentences = get_number_of_negative_sentences(app_id, conn)
    neutral_sentences = get_number_of_neutral_sentences(app_id, conn)
    sentences = [positive_sentences, negative_sentences, neutral_sentences]

    tab1, tab2, tab3 = st.tabs(["📄 Overview", "📊 Aspect Based Sentiment Analysis", "💭 Top Opinions"])

    with tab1:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Number of Reviews",
                f"{sum(review_numbers):,}"
            )

        with col2:
            st.metric(
                "Number of Opinions",
                f"{sum(sentences):,}"
            )


        with col3:
            avg_rating = sum([i * n for i, n in enumerate(review_numbers, 1)]) / sum(review_numbers)
            st.metric(
                "Average Star Rating",
                f"{avg_rating:.2f}"
            )

        with col4:
            total_aspects = len(selected_options)
            st.metric(
                "Aspects Analyzed",
                f"{total_aspects}"
            )

        # Your existing charts with enhanced styling
        st.divider()
        col1, col2 = st.columns(2)

        # Create a DataFrame
        review_source = pd.DataFrame({"ratings": [1, 2, 3, 4, 5], "review_numbers": review_numbers})

        sentence_source = pd.DataFrame({"sentiments": [1, -1, 0], "sentences": sentences})

        rating_colors = {
            5: '#3468eb',  # Dark blue
            4: '#34b1eb',  # Light blue
            3: '#a8eb34',  # Orange
            2: '#ebc934',  # Golden yellow
            1: '#eb4f34'  # Red
        }

        sentiment_colors = {
            -1: '#eb4f34',
            0: '#a8eb34',
            1: '#3468eb'
        }

        # Create color sequence based on ratings
        color_sequence = [rating_colors[rating] for rating in sorted(review_source['ratings'])]

        # # Plotting
        # review_figure = px.pie(review_source, names='ratings', values='review_numbers', hole=0.3,
        #                        title='Review Distribution by Star Ratings',
        #                        color_discrete_sequence= color_sequence,
        #                        # Custom color sequence
        #                        labels={'ratings': 'Star Rating', 'review_numbers': 'Number of Reviews'}  # Better labels
        #                        )
        #
        # review_figure.update_layout(legend_title_text='Star Ratings')

        # Create the figure
        review_figure = go.Figure(
            data=[go.Pie(
                labels=review_source['ratings'],
                values=review_source['review_numbers'],
                hole=0.3,
                marker=dict(colors=[rating_colors[rating] for rating in review_source['ratings']]),
                textinfo='percent+value'
            )]
        )

        review_figure.update_layout(title="Review Star Rating Distribution",legend_title_text='Star Ratings')

        review_figure.write_image("review_figure.png")


        # Plotting
        opinion_figure = go.Figure(
            data = [go.Pie(
                labels = sentence_source['sentiments'],
                values = sentence_source['sentences'],
                hole=0.3,
                marker=dict(colors=[sentiment_colors[sentiment] for sentiment in sentence_source['sentiments']]),
                textinfo='percent+value'
            )]
        )

        opinion_figure.update_layout(title="Opinion Sentiment Distribution",legend_title_text='Sentiments')

        opinion_figure.write_image("opinion_figure.png")

        with col1:
            st.plotly_chart(review_figure, use_container_width=True)

        with col2:
            st.plotly_chart(opinion_figure, use_container_width=True)

    with tab2:
        aspect_positive_list = []
        aspect_negative_list = []
        aspect_neutral_list = []
        selected_aspect_ids = []

        for aspect in selected_options:
            aspect_id = get_aspect_id(aspect, conn)
            selected_aspect_ids.append(aspect_id)

        for aspect_id in selected_aspect_ids:
            aspect_positive_list.append(get_aspect_senti_positive(aspect_id, conn))
            aspect_neutral_list.append(get_aspect_senti_neutral(aspect_id, conn))
            aspect_negative_list.append(get_aspect_senti_negative(aspect_id, conn))

        # Creating the Stacked Bar Chart
        aspect_figure = go.Figure()

        aspect_figure.add_trace(go.Bar(
            y=selected_options,
            x=aspect_positive_list,
            name='Positive',
            orientation='h'
        ))

        aspect_figure.add_trace(go.Bar(
            y=selected_options,
            x=aspect_negative_list,
            name='Negative',
            orientation='h'
        ))

        aspect_figure.add_trace(go.Bar(
            y=selected_options,
            x=aspect_neutral_list,
            name='Neutral',
            orientation='h'
        ))

        # Update layout to make it a stacked bar chart
        aspect_figure.update_layout(
            barmode='stack',
            title='Aspects vs Number of Opinions by Sentiments',
            xaxis_title='Number of Opinions',
            yaxis_title='Aspects',
            template='plotly',
            height=1000
        )

        aspect_figure.update_layout(barmode='stack')
        st.plotly_chart(aspect_figure, use_container_width=True)

        aspect_figure.write_image("aspect_figure.png")

    with tab3:
        my_multidict = MultiDict()

        match number_of_opinion:
            case 1:
                for aspect_id in selected_aspect_ids:
                    opinions = list()
                    aspect_name = get_aspect_name(aspect_id, conn)

                    if get_aspect_sentence_summary(aspect_id, 5, conn) is not None:
                        opinions.append(get_aspect_sentence_summary(aspect_id, 5, conn))
                    else:
                        opinions.append(" ")
                    my_multidict.add(aspect_name, opinions[0])

            case 2:
                for aspect_id in selected_aspect_ids:
                    opinions = list()
                    aspect_name = get_aspect_name(aspect_id, conn)

                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 5, conn) if get_aspect_sentence_summary(aspect_id, 5,
                                                                                                       conn) is not None else " ")
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 4, conn) if get_aspect_sentence_summary(aspect_id, 4,
                                                                                                       conn) is not None else " ")

                    my_multidict.add(aspect_name, opinions[0])
                    my_multidict.add(aspect_name, opinions[1])

            case 3:
                for aspect_id in selected_aspect_ids:
                    opinions = list()
                    aspect_name = get_aspect_name(aspect_id, conn)
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 5, conn) if get_aspect_sentence_summary(aspect_id, 5,
                                                                                                       conn) is not None else " ")
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 4, conn) if get_aspect_sentence_summary(aspect_id, 4,
                                                                                                       conn) is not None else " ")
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 3, conn) if get_aspect_sentence_summary(aspect_id, 3,
                                                                                                       conn) is not None else " ")

                    my_multidict.add(aspect_name, opinions[0])
                    my_multidict.add(aspect_name, opinions[1])
                    my_multidict.add(aspect_name, opinions[2])

            case 4:
                for aspect_id in selected_aspect_ids:
                    opinions = list()
                    aspect_name = get_aspect_name(aspect_id, conn)
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 5, conn) if get_aspect_sentence_summary(aspect_id, 5,
                                                                                                       conn) is not None else " ")
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 4, conn) if get_aspect_sentence_summary(aspect_id, 4,
                                                                                                       conn) is not None else " ")
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 3, conn) if get_aspect_sentence_summary(aspect_id, 3,
                                                                                                       conn) is not None else " ")
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 2, conn) if get_aspect_sentence_summary(aspect_id, 2,
                                                                                                       conn) is not None else " ")
                    my_multidict.add(aspect_name, opinions[0])
                    my_multidict.add(aspect_name, opinions[1])
                    my_multidict.add(aspect_name, opinions[2])
                    my_multidict.add(aspect_name, opinions[3])

            case 5:
                for aspect_id in selected_aspect_ids:
                    opinions = list()
                    aspect_name = get_aspect_name(aspect_id, conn)
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 5, conn) if get_aspect_sentence_summary(aspect_id, 5,
                                                                                                       conn) is not None else " ")
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 4, conn) if get_aspect_sentence_summary(aspect_id, 4,
                                                                                                       conn) is not None else " ")
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 3, conn) if get_aspect_sentence_summary(aspect_id, 3,
                                                                                                       conn) is not None else " ")
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 2, conn) if get_aspect_sentence_summary(aspect_id, 2,
                                                                                                       conn) is not None else " ")
                    opinions.append(
                        get_aspect_sentence_summary(aspect_id, 1, conn) if get_aspect_sentence_summary(aspect_id, 1,
                                                                                                       conn) is not None else " ")
                    my_multidict.add(aspect_name, opinions[0])
                    my_multidict.add(aspect_name, opinions[1])
                    my_multidict.add(aspect_name, opinions[2])
                    my_multidict.add(aspect_name, opinions[3])
                    my_multidict.add(aspect_name, opinions[4])

            case _:
                print("Error!")

        d = {'aspect': my_multidict.keys(), 'opinion': my_multidict.values()}
        df = pd.DataFrame(data=d)

        summary_table = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        line_color='darkslategray',
                        fill_color='lightskyblue',
                        align='left'),
            cells=dict(values=[df['aspect'], df['opinion']],
                       line_color='darkslategray',
                       fill_color='lightcyan',
                       align='left'))
        ])

        # Update layout to make it a stacked bar chart
        summary_table.update_layout(
            title = "Aspects and Top Opinions",
            height=1000
        )

        st.plotly_chart(summary_table, use_container_width=True)

        summary_table.write_image("summary_table.png")


    def generate_pdf(df, user_option, selected_options, selected_start_date, selected_end_date,
                         number_of_opinion, review_numbers, sentences):

        # Initialize PDF with custom table support
        pdf = PDFTable()
        pdf.set_auto_page_break(True, margin=10)

        # Add title page
        pdf.add_page()
        pdf.set_font("Arial", "BU", size=16)
        pdf.cell(190, 10, txt="Analysis Summary Report", ln=True, align='C')
        pdf.ln(30)

        # Add metadata
        metadata_items = [
            ("Report Date", datetime.now().strftime("%Y/%m/%d %H:%M")),
            ("Analyzed Application", user_option),
            ("Analyzed Date Interval", f"from {selected_start_date} to {selected_end_date}"),
            ("Average Rating", f"{avg_rating:.2f}"),
            ("Number of Reviews", sum(review_numbers)),
            ("Number of Opinions", sum(sentences)),
            ("Top Opinion Count", number_of_opinion),
            ("Analyzed Aspects", ', '.join(selected_options))
        ]

        pdf.set_font("Arial", "B", 12)
        for label, value in metadata_items:
            pdf.cell(60, 8, txt=f"{label}:", ln=0)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(130, 8, txt=str(value))
            pdf.set_font("Arial", "B", 12)

        pdf.ln(30)

        pdf.image('review_figure.png', x=10, y=pdf.get_y(), w=95)
        pdf.image('opinion_figure.png', x=110, y=pdf.get_y(), w=95)

        # Add aspect sentiments chart on new page
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Aspect Based Sentiments", ln=True, align='C')
        pdf.ln(5)
        pdf.image('aspect_figure.png', x=20, y=None, w=170)

        # Add opinion table on next page
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Top Opinions", ln=True, align='C')
        pdf.ln(5)

        # Create the table
        pdf.create_table(
            df,
            row_height=7,
            font_size=9,
            header_font_size=11
        )

        # Save the PDF
        output_filename = "analysis_report.pdf"
        pdf.output(output_filename)
        return output_filename

    with st.sidebar:
        if st.button("Generate Report"):
            generate_pdf(df, user_option, selected_options, selected_start_date, selected_end_date,
                         number_of_opinion, review_numbers, sentences)
            st.toast("Report generated successfully!")
            with open("analysis_report.pdf", "rb") as f:
                st.download_button("Download Report", f, "report.pdf")

if __name__ == "__main__":
    main()