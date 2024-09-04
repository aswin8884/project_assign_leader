from django.shortcuts import render,redirect,get_object_or_404
from .models import*
from django.contrib.auth import authenticate
from django.contrib import messages
from django.utils import timezone
from datetime import date,timedelta
from django.db.models import Q

def login(request):

    if request.POST:
        email=request.POST['email']
        password=request.POST['password']

        user=authenticate(username=email,password=password)

        if user:
            if user.is_active:
                if user.is_superuser:
                    return redirect('/admin_home')
                elif user.usertype=="leader":
                    user = Add_leader.objects.get(email=email)
                    request.session["email"] = email
                    request.session["id"] = user.id
                    return redirect('/leader_home')
                
                elif user.usertype=="member":
                    user = Add_member.objects.get(email=email)
                    request.session["email"] = email
                    request.session["id"] = user.id
                    return redirect('/member_home')
                

    return render(request,"login.html")


################### ADMIN ##########################

def admin_home(request):

    leader=Add_leader.objects.all()
    projects=Add_project.objects.all()
    completed=projects.filter(completed=True)

    leaders_count=leader.count()
    projects_count=projects.count()
    completed_count=completed.count()
    pending_count=projects_count-completed_count


    return render(request,"admin/admin_home.html",{
        "leaders_count":leaders_count,
        "projects_count":projects_count,
        "completed_count":completed_count,
        "pending_count":pending_count,
        })


def add_leaders_admin(request):

    if request.POST:
        name=request.POST['name']
        team_name=request.POST['team_name']
        job_name=request.POST['job_name']
        employee_id=request.POST['employee_id']
        contact=request.POST['contact']
        email=request.POST['email']
        password=request.POST['password']
        profile_picture=request.FILES['profile_picture']

        log=Login_table.objects.create_user(username=email,password=password,usertype="leader")
        log.save()

        leader=Add_leader.objects.create(
            name=name,
            team_name=team_name,
            job_name=job_name,
            employee_id=employee_id,
            contact=contact,
            email=email,
            profile_picture=profile_picture,
            login_id=log
        )
        leader.save()
        messages.info(request,"Leader added successfully")

    return render(request,"admin/add_leaders.html")

def view_leaders_admin(request):

    leaders=Add_leader.objects.all()

    return render(request,"admin/view_leaders.html",{"leaders":leaders})

def update_leader_admin(request):
    lid=request.GET.get('id')
    leader=Add_leader.objects.get(id=lid)

    if request.POST:
        name=request.POST["name"]
        leader.name=name
        team_name=request.POST["team_name"]
        leader.team_name=team_name
        job_name=request.POST["job_name"]
        leader.job_name=job_name
        employee_id=request.POST["employee_id"]
        leader.employee_id=employee_id
        contact=request.POST["contact"]
        leader.contact=contact
        profile_picture=request.FILES["profile_picture"]
        leader.profile_picture=profile_picture

        messages.info(request,"Updated successfully")
        leader.save()
        return redirect('/view_leaders_admin')


    return render(request,'admin/update_leader_details.html',{"leader":leader})

def delete_leader_admin(request):

    lid=request.GET.get('id')
    leader=Add_leader.objects.get(id=lid)
    leader.delete()
    log=Login_table.objects.get(username=leader.login_id)
    log.delete()
    messages.info(request,"Successfully removed")

    return redirect('/view_leaders_admin')

################### LEADER ##########################

def leader_home(request):

    id=request.session['id']
    members=Add_member.objects.filter(leader_id=id)
    projects=Add_project.objects.filter(leader_id=id)
    members_count=0
    projects_count=0
    completed_count=0
    pending_count=0

    for m in members:
        members_count+=1

    for p in projects:
        projects_count+=1
      
    for c in projects:
        if c.completed:
            completed_count+=1
            
    for a in projects:
        if a.completed == False:
            pending_count+=1

    return render(request,"leader/leader_home.html",{
        "members_count":members_count,
        "projects_count":projects_count,
        "completed_count":completed_count,
        "pending_count":pending_count,
        })

def add_members_leader(request):

    id=request.session['id']
    leader=Add_leader.objects.get(id=id)

    if request.POST:
        name=request.POST['name']
        job_name=request.POST['job_name']
        employee_id=request.POST['employee_id']
        contact=request.POST['contact']
        email=request.POST['email']
        password=request.POST['password']
        profile_picture=request.FILES['profile_picture']

        log=Login_table.objects.create_user(username=email,password=password,usertype="member")
        log.save()

        member=Add_member.objects.create(
            name=name,
            job_name=job_name,
            employee_id=employee_id,
            contact=contact,
            email=email,
            profile_picture=profile_picture,
            leader_id=leader,
            login_id=log
        )
        member.save()
        messages.info(request,"Team member added successfully")

    return render(request,"leader/add_members.html")

def view_members_leader(request):

    id=request.session['id']
    members=Add_member.objects.filter(leader_id=id)

    return render(request,"leader/view_members.html",{"members":members})

def update_member_leader(request):

    mid=request.GET.get('id')
    member=Add_member.objects.get(id=mid)

    if request.POST:
        name=request.POST["name"]
        member.name=name
        job_name=request.POST["job_name"]
        member.job_name=job_name
        employee_id=request.POST["employee_id"]
        member.employee_id=employee_id
        contact=request.POST["contact"]
        member.contact=contact
        profile_picture=request.FILES["profile_picture"]
        member.profile_picture=profile_picture

        messages.info(request,"Updated successfully")
        member.save()
        return redirect('/view_members_leader')


    return render(request,'leader/update_member_details.html',{"member":member})

def delete_member_leader(request):
    mid = request.GET.get('id')
    member = Add_member.objects.get(id=mid)

    # Find all projects associated with this member and set the corresponding field to null
    Add_project.objects.filter(first_member_id=member).update(first_member_id=None)
    Add_project.objects.filter(second_member_id=member).update(second_member_id=None)
    Add_project.objects.filter(third_member_id=member).update(third_member_id=None)
    Add_project.objects.filter(fourth_member_id=member).update(fourth_member_id=None)
    Add_project.objects.filter(fifth_member_id=member).update(fifth_member_id=None)

    
    member.delete()

 
    log = Login_table.objects.get(username=member.login_id)
    log.delete()

    messages.info(request, "Successfully removed")

    return redirect('/view_members_leader')


def add_projects_leader(request):

    id=request.session['id']
    leader=Add_leader.objects.get(id=id)

    if request.POST:
        title=request.POST['title']
        description=request.POST['description']
        submission_date=request.POST['submission_date']
        project_image=request.FILES['project_image']

        project=Add_project.objects.create(
            title=title,
            description=description,
            submission_date=submission_date,
            project_image=project_image,
            uploaded_date=timezone.now(),
            leader_id=leader
        )
        project.save()
        messages.info(request,"Work added successfully")

    return render(request,"leader/add_projects.html")

def update_project_leader(request):

    pid=request.GET.get('id')
    project=Add_project.objects.get(id=pid)

    if request.POST:
        title=request.POST["title"]
        project.title=title
        description=request.POST["description"]
        project.description=description
        project_image=request.FILES["project_image"]
        project.project_image=project_image
        submission_date=request.POST["submission_date"]
        project.submission_date=submission_date

        project.uploaded_date=timezone.now()

        project.save()
        messages.info(request,"Updated successfully")

        return redirect('/view_projects_leader')


    return render(request,"leader/update_project_leader.html",{"project":project})

def delete_project_leader(request):

    pid=request.GET.get('id')
    project=Add_project.objects.get(id=pid)
    project.delete()
    messages.info(request,"Deleted successfully")

    return redirect('/view_projects_leader')

def view_projects_leader(request):

    id=request.session['id']
    projects=Add_project.objects.filter(leader_id=id)
    
    return render(request,"leader/view_projects.html",{"projects":projects})

def view_projects_leader_single(request):

    pid=request.GET.get('id')
    project=Add_project.objects.get(id=pid)
    
    return render(request,"leader/view_projects_single.html",{"project":project})

def assign_projects_leader(request):

    id=request.session['id']
    members=Add_member.objects.filter(leader_id=id)
    projects=Add_project.objects.filter(leader_id=id)

    return render(request,"leader/assign_projects.html",{"members":members,"projects":projects})

def assign_project(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        project_id = request.POST.get('project_id')

        try:
            member = Add_member.objects.get(id=member_id)
            project = Add_project.objects.get(id=project_id)
        except (Add_member.DoesNotExist, Add_project.DoesNotExist):
            messages.error(request, "Member or Project does not exist")
            return redirect('/assign_projects_leader')

        # Check if the member is already assigned to the project
        if (project.first_member_id == member or
            project.second_member_id == member or
            project.third_member_id == member or
            project.fourth_member_id == member or
            project.fifth_member_id == member):
            messages.error(request, "This member is already assigned to the project")
            return redirect('/assign_projects_leader')

        # Assign the member to the first available slot
        if not project.first_member_id:
            project.first_member_id = member
        elif not project.second_member_id:
            project.second_member_id = member
        elif not project.third_member_id:
            project.third_member_id = member
        elif not project.fourth_member_id:
            project.fourth_member_id = member
        elif not project.fifth_member_id:
            project.fifth_member_id = member
        else:
            messages.error(request, "All member slots are full")
            return redirect('/assign_projects_leader')

        member.assigned_status = True
        member.save()
        project.assigned = True
        project.save()

        messages.info(request, "Work assigned successfully")
        return redirect('/assign_projects_leader')

    messages.error(request, "Invalid request method")
    return redirect('/assign_projects_leader')


def view_progress_leader(request):
    leader_id = request.session['id']
    leader = Add_leader.objects.get(id=leader_id)
    if leader_id:
        projects = Add_project.objects.filter(leader_id=leader)
    else:
        projects = Add_project.objects.none()  

    return render(request, 'leader/view_progress.html', {"projects": projects})

def approve_work_leader(request):

    pid=request.GET.get('id')
    project=Add_project.objects.get(id=pid)
    project.leader_approvel=True
    project.leader_rejected=False
    project.save()
    messages.info(request,"Project Approved")

    return redirect('/view_progress_leader')

def reject_work_leader(request):

    pid=request.GET.get('id')
    project=Add_project.objects.get(id=pid)

    project.progress=0
    project.completed=False
    project.completed_date=None
    project.leader_rejected=True
    project.save()
    messages.info(request,"Project rejected")

    return redirect('/view_progress_leader')

def view_project_members_leader(request):
    pid = request.GET.get('id')
    project = Add_project.objects.get(id=pid)
    
    members = [
        project.first_member_id,
        project.second_member_id,
        project.third_member_id,
        project.fourth_member_id,
        project.fifth_member_id
    ]

    members = [member for member in members if member is not None]

    return render(request, "leader/view_project_members.html", {"project": project, "members": members})

def view_completed_work_leader(request):

    pid=request.GET.get('id')
    project=Add_project.objects.get(id=pid)

    members = [
        project.first_member_id,
        project.second_member_id,
        project.third_member_id,
        project.fourth_member_id,
        project.fifth_member_id
    ]

    members = [member for member in members if member is not None]

    return render(request,"leader/view_completed_work.html",{"project":project,"members": members})



################### MEMBER ##########################

def member_home(request):
    # Get the member's ID from the session
    id = request.session['id']

    # Filter projects where the member is involved
    projects = Add_project.objects.filter(
        first_member_id=id
    ) | Add_project.objects.filter(
        second_member_id=id
    ) | Add_project.objects.filter(
        third_member_id=id
    ) | Add_project.objects.filter(
        fourth_member_id=id
    ) | Add_project.objects.filter(
        fifth_member_id=id
    )

    # Initialize counters
    projects_count = projects.count()
    completed_count = projects.filter(completed=True).count()
    pending_count = projects_count - completed_count

    return render(request, "member/member_home.html", {
        "projects_count": projects_count,
        "completed_count": completed_count,
        "pending_count": pending_count,
    })

def view_works_member(request):
    member_id = request.session.get('id')
    
    if member_id:
        works = Add_project.objects.filter(
            Q(first_member_id=member_id) |
            Q(second_member_id=member_id) |
            Q(third_member_id=member_id) |
            Q(fourth_member_id=member_id) |
            Q(fifth_member_id=member_id)
        )
    else:
        works = Add_project.objects.none() 

    return render(request, "member/view_works.html", {"works": works})

def add_progress_member(request):
    wid = request.GET.get('id')
    member_id = request.session.get('id')
    
    try:
        project = Add_project.objects.get(id=wid)
    except Add_project.DoesNotExist:
        messages.error(request, "Project does not exist.")
        return redirect('/view_works_member')


    if not (project.first_member_id_id == member_id or 
            project.second_member_id_id == member_id or 
            project.third_member_id_id == member_id or 
            project.fourth_member_id_id == member_id or 
            project.fifth_member_id_id == member_id):
        messages.error(request, "You are not authorized to update the progress of this project.")
        return redirect('/view_works_member')


    if project.progress < 100:
        project.progress = min(project.progress + 25, 100)
        project.save()
        messages.info(request, "Progress updated successfully.")
    else:
        messages.info(request, "Project is already complete.")

    return redirect(f'/view_works_single_member?id={project.id}')

def view_works_single_member(request):

    id=request.session['id']
    member=Add_member.objects.get(id=id)
    wid=request.GET.get('id')
    work=Add_project.objects.get(id=wid)
    comments=Add_comment.objects.filter(project_id=work)
    # Calculate the days left until the submission deadline
    today = timezone.now().date()  # This gives the current date
    submission_date = work.submission_date.date()  # Convert datetime to date

    # Subtract two date objects to get the number of days left
    days_left = (submission_date - today).days
    is_past_deadline = days_left < 0

    return render(request,"member/view_work_single.html",
        {
        'work': work,
        'comments': comments,
        'days_left': days_left,
        'is_past_deadline': is_past_deadline,
        "member":member
        })

def submit_work_member(request):

    sid=request.GET.get('id')
    work=Add_project.objects.get(id=sid)
    work.completed=True
    work.completed_date=timezone.now()
    work.save()

    return redirect(f'/view_works_single_member?id={work.id}')

def add_comment_members(request):
    id=request.session['id']
    mid=Add_member.objects.get(id=id)

    if request.POST:
        comment=request.POST['comment']
        project_id=request.POST['project_id']

        project=Add_project.objects.get(id=project_id)

        c=Add_comment.objects.create(
            comment=comment,
            member_id=mid,
            project_id=project,
            sent_by=timezone.now()
        )
        c.save()
        messages.info(request,"Comment sent successfully")

    return redirect(f'/view_works_single_member?id={project.id}')

