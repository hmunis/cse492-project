from fpdf import FPDF


class PDFTable(FPDF):

    def create_table(
            self,
            df,
            col_widths=None,
            row_height=7,
            font_size=9,
            header_font_size=10,
            max_cell_height=50,
            table_x=None,
            table_y=None
    ):
        # set table position
        if table_x is not None and table_y is not None:
            self.set_xy(table_x, table_y)

        # calculate column widths
        if col_widths is None:
            page_width = self.w - 2 * self.l_margin
            col_widths = [page_width * 0.2,
                          page_width * 0.8]  # 20% for aspect, 80% for opinion

        def get_cell_height(text, width):
            self.set_font('Arial', size=font_size)
            lines = str(text).split('\n')
            total_height = 0
            for line in lines:
                str_width = self.get_string_width(line)
                lines_needed = max(1, str_width / (width - 2))
                total_height += row_height * lines_needed
            return min(max_cell_height, total_height)


        self.set_font('Arial', 'B', header_font_size)
        self.set_fill_color(240, 240, 240)
        for i, col_name in enumerate(df.columns):
            self.cell(col_widths[i], row_height, str(col_name), 1, 0, 'C', fill=True)
        self.ln()


        self.set_font('Arial', size=font_size)
        self.set_fill_color(255, 255, 255)

        for _, row in df.iterrows():
            row_heights = [get_cell_height(cell, col_widths[i]) for i, cell in enumerate(row)]
            max_height = max(row_heights)


            if self.get_y() + max_height > self.page_break_trigger:
                self.add_page()

            x_start = self.get_x()
            y_start = self.get_y()


            for i, cell in enumerate(row):
                self.set_xy(x_start + sum(col_widths[:i]), y_start)


                if i == 1:
                    cell_text = ' '.join(str(cell).split())
                    self.multi_cell(
                        col_widths[i],
                        row_height,
                        cell_text,
                        1,
                        'L',
                        fill=True
                    )
                else:
                    self.cell(
                        col_widths[i],
                        max_height,
                        str(cell),
                        1,
                        0,
                        'L',
                        fill=True
                    )


            self.set_xy(x_start, y_start + max_height)
            self.ln(0)

        return self.get_y()



