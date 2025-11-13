from .models import OrganizationInfo, ContactInfo

def organization_info(request):
    org_info = OrganizationInfo.objects.first()
    contact_info = ContactInfo.objects.first()  
    
    return {
        'org_info': org_info,
        'contact_info': contact_info
    }