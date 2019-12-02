class Camera {
    constructor(lookFrom, lookAt, up, fov, aspect, focusDist) {
        this.up = up.normalized();
        this.origin = lookFrom;
        this.direction = lookAt.subtract(lookFrom).normalized();
        
        let theta = fov * Math.PI / 180;
        let halfHeight = Math.tan(theta / 2);
        let halfWidth = halfHeight * aspect;
        
        this.right = this.up.cross(this.direction).normalized();
        const corner = this.right.multiply(halfWidth * focusDist).add(this.up.multiply(halfHeight * focusDist)).subtract(this.direction.multiply(focusDist));
        this.bottomLeftCorner = this.origin.subtract(corner);
        this.horizontal = this.right.multiply(2 * halfWidth * focusDist);
        this.vertical = this.up.multiply(2 * halfHeight * focusDist);
    }
    
    getRay(u,v) {
        return new Ray(this.origin, this.bottomLeftCorner.add(this.horizontal.multiply(u)).add(this.vertical.multiply(v)).subtract(this.origin))
    }
}