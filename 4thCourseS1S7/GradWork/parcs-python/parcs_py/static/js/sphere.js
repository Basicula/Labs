class Sphere {
    constructor(center,radius,material) {
        this.center = center;
        this.radius = radius;
        this.material = material;
    }
    
    /*
    System for intersection:
    O + D*t = P;
    (P - C)*(P - C) = R^2
    Then we have one quadratic equation:
    (O + D*t - C) * (O + D*t - C) = R^2 => (O - C + D*t) * (O - C + D*t) = R^2
    or
    D^2 * t^2 + 2 * (O - C) * D * t + (O - C)^2 - R^2 = 0
    */
    hit(ray,hit) {
        const o_c = ray.origin.subtract(this.center);
        const d_o_c = ray.direction.dot(o_c);
        const r_sqr = this.radius * this.radius;
        const d = d_o_c * d_o_c - (o_c.lengthSqr() - r_sqr);
        if(d < 0)
            return false;
        hit.distance = (-d_o_c - Math.sqrt(d));
        hit.intersection = ray.origin.add(ray.direction.multiply(hit.distance));
        hit.normal = hit.intersection.subtract(this.center).normalized();
        hit.material = this.material;
        return true;
    }
}