from . import admin
from .views import *

# 辅助URL
admin.add_url_rule('/document/<filename>', view_func=render_file)
admin.add_url_rule('c2data', view_func=change_select_field, methods=['POST'])
admin.add_url_rule('unit_data', view_func=change_unit_field, methods=['POST'])
admin.add_url_rule('case/pic', view_func=case_pic, methods=['POST'])
admin.add_url_rule('index/bar', view_func=index_bar, methods=['POST'])
admin.add_url_rule('index/line', view_func=index_line, methods=['POST'])
admin.add_url_rule('profile/', view_func=profile)
admin.add_url_rule('index/', view_func=index)
admin.add_url_rule('upload/', view_func=upload, methods=['POST'])
# 问题管理URL
admin.add_url_rule('add/', view_func=AddView.as_view('content_add'))
admin.add_url_rule('del/<int:id>/', view_func=DelView.as_view('content_delete'))
admin.add_url_rule('detail/', view_func=DetailView.as_view('content_detail'))
admin.add_url_rule('edit/', view_func=UpdateView.as_view('content_edit'))
admin.add_url_rule('detail/export/', view_func=ExportView.as_view('export_data'))
admin.add_url_rule('analysis/', view_func=AnalysisView.as_view('content_analysis'))
# 文件管理URL
admin.add_url_rule('document_upload/', view_func=DocumentUploadOrEdit.as_view('document_upload'))
admin.add_url_rule('document_edit/<int:id>', view_func=DocumentUploadOrEdit.as_view('document_edit'))
admin.add_url_rule('document_detail/', view_func=DocumentDetail.as_view('document_detail'))
admin.add_url_rule('document_delete/<int:id>', view_func=DocumentDelete.as_view('document_delete'))
# 表扬管理URL
admin.add_url_rule('praise_detail/', view_func=PraiseDetailView.as_view('praise_detail'))
admin.add_url_rule('praise_add/', view_func=PraiseAddView.as_view('praise_add'))
admin.add_url_rule('praise_del/<int:id>/', view_func=PraiseDelView.as_view('praise_delete'))