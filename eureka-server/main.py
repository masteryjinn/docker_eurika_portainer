from fastapi import FastAPI, Request, Response
import xml.etree.ElementTree as ET

app = FastAPI(title="Eureka Server Mock")

registry = {}

@app.post("/eureka/apps/{app_name}")
async def register(app_name: str, request: Request):
    body = await request.json()
    instance = body.get("instance", {})
    instance_id = instance.get("instanceId", "unknown")
    registry[instance_id] = {
        "app": app_name.upper(),
        "hostName": instance.get("hostName"),
        "port": instance.get("port", {}).get("$", 80)
    }
    return {"status": "Accepted"}

@app.put("/eureka/apps/{app_name}/{instance_id}")
async def renew_lease(app_name: str, instance_id: str):
    return Response(status_code=200)

@app.delete("/eureka/apps/{app_name}/{instance_id}")
async def deregister(app_name: str, instance_id: str):
    if instance_id in registry:
        del registry[instance_id]
    return {"status": "OK"}

def generate_apps_xml():
    xml_root = ET.Element("applications")
    apps_dict = {}
    for inst_id, data in registry.items():
        app_name = data["app"]
        if app_name not in apps_dict:
            apps_dict[app_name] = []
        apps_dict[app_name].append((inst_id, data))
    
    for app_name, instances in apps_dict.items():
        app_elem = ET.SubElement(xml_root, "application")
        name_elem = ET.SubElement(app_elem, "name")
        name_elem.text = app_name
        
        for inst_id, inst in instances:
            inst_elem = ET.SubElement(app_elem, "instance")
            id_elem = ET.SubElement(inst_elem, "instanceId")
            id_elem.text = inst_id
            host_elem = ET.SubElement(inst_elem, "hostName")
            host_elem.text = inst["hostName"]
            port_elem = ET.SubElement(inst_elem, "port", {"enabled": "true"})
            port_elem.text = str(inst["port"])
            status_elem = ET.SubElement(inst_elem, "status")
            status_elem.text = "UP"

    return ET.tostring(xml_root, encoding="utf-8", method="xml")

@app.get("/eureka/apps")
@app.get("/eureka/apps/")
def get_registry_xml():
    return Response(content=generate_apps_xml(), media_type="application/xml")

@app.get("/eureka/apps/delta")
@app.get("/eureka/apps/delta/")
def get_delta_xml():
    # Клієнт запитує дельту оновлень, віддаємо поточний стан у форматі XML
    return Response(content=generate_apps_xml(), media_type="application/xml")

@app.get("/")
def home():
    return {"system": "Eureka Server Mock", "registered_instances": registry}