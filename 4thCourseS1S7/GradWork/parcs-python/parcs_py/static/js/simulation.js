var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");
let it = 0;
let run = false;

function setPixel(data, width, x, y, r, g, b, a = 255) {
    const pixel_id = (y * width + x) * 4;
    data[pixel_id + 0] = r;
    data[pixel_id + 1] = g;
    data[pixel_id + 2] = b;
    data[pixel_id + 3] = a;
}

function getColor(hit, light, view) {
    const to_light = light.subtract(hit.intersection).normalized();
    const to_view = view.subtract(hit.intersection).normalized();
    const diffuse = Math.max(0,hit.normal.dot(to_light));
    const specular = Math.pow(Math.max(0.0, hit.normal.multiply(hit.normal.dot(to_light) * 2).subtract(to_light).dot(to_view)), hit.material.shinines);
    const m = hit.material;
    const red = m.ambient.x + m.diffuse.x * diffuse + m.specular.x * specular;
    const green = m.ambient.y + m.diffuse.y * diffuse + m.specular.y * specular;
    const blue = m.ambient.z + m.diffuse.z * diffuse + m.specular.z * specular;
    return new Vertex3D(m.color.x * red, m.color.y * green, m.color.z * blue);
}

function render() {
    const width = canvas.width;
    const height= canvas.height;
    
    let image = context.getImageData(0, 0, width, height);
    
    let material = new Material(new Vertex3D(255,0,0), new Vertex3D(0.1745, 0.01175, 0.01175), new Vertex3D(0.61424, 0.04136, 0.04136), new Vertex3D(0.727811, 0.626959, 0.626959),76.8);
    let camera = new Camera(new Vertex3D(0,0,0), new Vertex3D(0,0,1), new Vertex3D(0,1,0), 60, width/height, 1);
    let sphere = new Sphere(new Vertex3D(5,0,20), 2, material);
    let light = new Vertex3D(0,5,15);
    
    sphere.center.x = 5 * Math.cos(it);
    sphere.center.z = 15 + 5 * Math.sin(it);
    light.y += Math.random()*5-10;
    
    for(let y = 0; y < height; ++y) {
        for (let x = 0; x < width; ++x) {
            let hit = new Hit();
            let ray = camera.getRay(x/width, y/height);
            if(sphere.hit(ray,hit) && hit.isCorrect()) {
                const color = getColor(hit,light,ray.origin);
                setPixel(image.data, width, x, height - y, color.x,color.y,color.z);
            }
            else {
                setPixel(image.data, width, x, height - y, 0, 0, 0)
            }
        }
    }
    context.putImageData(image,0,0);
}

function play() {
    it+=0.1;
    render();
    if(run) {
        setTimeout(play,1);
    }
}

function click() {
    run = !run;
    if(run)
        play();
}

canvas.addEventListener('click', click, false);

