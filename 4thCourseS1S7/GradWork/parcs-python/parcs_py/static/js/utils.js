class Hit {
    constructor() {
        this.distance = -1;
        this.intersection = new Vertex3D(0,0,0);
        this.normal = new Vertex3D(0,0,0);
        this.material = new Material();
    }
    
    isCorrect() {
        return (this.distance >= 0);
    }
}