import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

public class DrawMandelbrot
{
    private static final int MAXITER = 32;
    private static final int WIDTH = 256;
    private static final int HEIGHT = 256;

    public void drawMandelbrot()
    {
        BufferedImage image = new BufferedImage(WIDTH, HEIGHT, BufferedImage.TYPE_INT_RGB);
        calcMandelbrot(image);
        writeImage(image);
    }

    private void writeImage(BufferedImage image)
    {
        try
        {
            ImageIO.write(image, "png", new File("mandel.png"));
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    private void calcMandelbrot(BufferedImage image)
    {
        double cy = -1.5;
        for (int y = 0; y < HEIGHT; y++)
        {
            double cx = -2.0;
            for (int x = 0; x < WIDTH; x++)
            {
                double zx = 0.0, zy = 0.0;
                int iter = calcIter(cy, cx, zx, zy);
                int rgb = calcRGBColor(iter);
                image.setRGB(x, y, rgb);
                cx += 3.0/WIDTH;
            }
            cy += 3.0/HEIGHT;
        }
    }

    private int calcRGBColor(int iter)
    {
        Color color = new Color(iter, (iter*256/16)&0xff, (iter*256/32)&0xff);
        int rgb = color.getRGB();
        return rgb;
    }

    private int calcIter(double cy, double cx, double zx, double zy)
    {
        double zzx = zx;
        double zzy = zy;
        int iter = 0;
        while (iter < MAXITER)
        {
            double zx2 = zzx * zzx;
            double zy2 = zzy * zzy;
            if (zx2 + zy2 > 4.0)
            {
                break;
            }
            zzy = 2.0 * zzx * zzy + cy;
            zzx = zx2 - zy2 + cx;
            iter ++;
        }
        return iter;
    }
    
    /**
     * @param args
     */
    public static void main(String[] args)
    {
        new DrawMandelbrot().drawMandelbrot();
    }

}
