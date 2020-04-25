import parcs.*;

public class Map implements AM{
    public void run(AMInfo info){
        long x,y,r;
        x = info.parent.readLong();
        System.out.print(x);
        y = info.parent.readLong();
        System.out.print('+');
        System.out.print(y);
        r = x+y;
        info.parent.write(r);
    }
}
