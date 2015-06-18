# [Markdown Checklist](https://github.com/FND/markdown-checklist)
# [![build status](https://secure.travis-ci.org/FND/markdown-checklist.png)](http://travis-ci.org/FND/markdown-checklist)
# [![coverage](https://coveralls.io/repos/FND/markdown-checklist/badge.png)](https://coveralls.io/r/FND/markdown-checklist)

# a [Python Markdown](http://pythonhosted.org/Markdown/) extension for lists of
# tasks with checkboxes

# inspired by
# [GitHub task lists](https://github.com/blog/1375-task-lists-in-gfm-issues-pulls-comments):

#     * [ ] foo
#     * [x] bar
#     * [ ] baz

# becomes

#     <ul>
#     <li><input type="checkbox" disabled> foo</li>
#     <li><input type="checkbox" disabled checked> bar</li>
#     <li><input type="checkbox" disabled> baz</li>
#     </ul>

# * a dash can be used instead of an asterisk for list items
# * both upper- and lowercase "x" are accepted to activate checkboxes


# Installation
# ------------

#     $ pip install markdown-checklist


# Usage
# -----

#     import markdown
#     html = markdown.markdown(source, extensions=['markdown_checklist.extension'])

# or

#     import markdown
#     from markdown_checklist.extension import ChecklistExtension
#     html = markdown.markdown(source, extensions=[ChecklistExtension()])

# There is also a small JavaScript/jQuery library to make checkboxes
# interactive:

#     new Checklists("article", function(checkbox, callback) {
#         var uri = checkbox.closest("article").find("h1 a").attr("href");
#         jQuery.get(uri, callback);
#     }, function(markdown, checkbox, callback) {
#         var uri = checkbox.closest("article").find("h1 a").attr("href");
#         jQuery.ajax({
#             type: "put",
#             uri: uri,
#             data: markdown,
#             success: callback
#         });
#     });

# See included `checklists.js` for details.
import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor


def makeExtension(configs=None):
    if configs is None:
        return ChecklistExtension()
    else:
        return ChecklistExtension(configs=configs)


class ChecklistExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add('checklist', ChecklistPostprocessor(md),
                              '>raw_html')


class ChecklistPostprocessor(Postprocessor):

    """
    adds checklist class to list element
    """

    pattern = re.compile(r'<li>\[([ Xx])\]')

    def run(self, html):
        html = re.sub(self.pattern, self._convert_checkbox, html)
        before = '<ul>\n<li><input type="checkbox"'
        after = before.replace('<ul>', '<ul class="checklist">')
        return html.replace(before, after)

    def _convert_checkbox(self, match):
        state = match.group(1)
        checked = ' checked' if state != ' ' else ''
        return '<li><input type="checkbox" disabled%s>' % checked
