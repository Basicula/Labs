import parcs.*;

public class Map implements AM{
    public void run(AMInfo info){
        long x,y,r;
        x = info.parent.readLong();
        y = info.parent.readLong();
        r = x+y;
        info.parent.write(r);
    }
}
