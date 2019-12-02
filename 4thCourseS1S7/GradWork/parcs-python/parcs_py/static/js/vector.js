class Vertex3D {
    constructor(x=0,y=0,z=0) {
        this.x = x;
        this.y = y;
        this.z = z;
    }
    
    clone() {
        return new Vertex3D(this.x, this.y, this.z);
    }
    
    negative() {
        return new Vertex3D(-this.x,-this.y,-this.z);
    }
    
    add(other) {
        if (other instanceof Vertex3D)
            return new Vertex3D(this.x + other.x, this.y + other.y, this.z + other.z);
        else 
            return new Vertex3D(this.x + other, this.y + other, this.z + other);
    }
    
    subtract(other) {
        if (other instanceof Vertex3D)
            return new Vertex3D(this.x - other.x, this.y - other.y, this.z - other.z);
        else 
            return new Vertex3D(this.x - other, this.y - other, this.z - other);
    }
    
    multiply(factor) {
        return new Vertex3D(this.x * factor, this.y * factor, this.z * factor);
    }
    
    divide(divider) {
        return new Vertex3D(this.x / divider, this.y / divider, this.z / divider);
    }
    
    dot(other) {
        return (this.x * other.x + this.y * other.y + this.z * other.z);
    }
    
    cross(other) {
        return new Vertex3D(
        this.y * other.z - other.y * this.z,
        this.x * other.z - other.x * this.z,
        this.x * other.y - other.x * this.y);
    }
    
    lengthSqr() {
        return this.dot(this);
    }
    
    length() {
        return Math.sqrt(this.lengthSqr());
    }
    
    normalize() {
        const length = this.length();
        if (length != 0) {
            this.x /= length;
            this.y /= length;
            this.z /= length;
        }
        return this;
    }
    
    normalized() {
        return this.clone().normalize();
    }
}