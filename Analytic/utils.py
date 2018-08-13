#get the ip address
def get_IP(request):
    forwaded_ip=request.META.get("HTTP_X_FORWARDED_FOR")
    if forwaded_ip:
        ip=forwaded_ip.split(",")[0]
    else:
        ip=request.META.get("REMOTE_ADDR")
    return ip