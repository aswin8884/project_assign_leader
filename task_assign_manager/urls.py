
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login),
    path('admin_home',views.admin_home),
    path('leader_home',views.leader_home),
    path('member_home',views.member_home),
    ############# Admin ##################
    path('member_home',views.member_home),
    path('add_leaders_admin',views.add_leaders_admin),
    path('view_leaders_admin',views.view_leaders_admin),
    path('update_leader_admin',views.update_leader_admin),
    path('delete_leader_admin',views.delete_leader_admin),
    ############# Leader ##################
    path('add_members_leader',views.add_members_leader),
    path('view_members_leader',views.view_members_leader),
    path('update_member_leader',views.update_member_leader),
    path('delete_member_leader',views.delete_member_leader),
    path('add_projects_leader',views.add_projects_leader),
    path('update_project_leader',views.update_project_leader),
    path('delete_project_leader',views.delete_project_leader),
    path('view_projects_leader',views.view_projects_leader),
    path('assign_projects_leader',views.assign_projects_leader),
    path('assign_project',views.assign_project),
    path('view_progress_leader',views.view_progress_leader),
    path('view_project_members_leader',views.view_project_members_leader),
    path('view_completed_work_leader',views.view_completed_work_leader),
    path('approve_work_leader',views.approve_work_leader),
    path('reject_work_leader',views.reject_work_leader),

    ############# Member ##################
    path('view_works_member',views.view_works_member),
    path('view_works_single_member',views.view_works_single_member),
    path('add_progress_member',views.add_progress_member),
    path('submit_work_member',views.submit_work_member),
    path('add_comment_members',views.add_comment_members),
]
