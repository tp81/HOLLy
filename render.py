""" # noqa
   ___           __________________  ___________
  / _/__  ____  / __/ ___/  _/ __/ |/ / ___/ __/
 / _/ _ \/ __/ _\ \/ /___/ // _//    / /__/ _/      # noqa
/_/ \___/_/   /___/\___/___/___/_/|_/\___/___/      # noqa
Author : Benjamin Blundell - k1803390@kcl.ac.uk

render.py - Spit out an image using our renderer, given
an obj file, sigma and optional rotation and translation.

"""

if __name__ == "__main__":
    """
    Render and save an image given a model.

    Given a model, rotation and a sigma, spit out an image for us.

    Parameters
    ----------
    sigma : float
        The sigma of the images in question - default 1.8
    obj : string
        The path to the obj file - default none.
    rot : string
        The rotation in angle/axis format - X,Y,Z.
        Pass in as a string with comma separation - default none.

    Returns
    -------
    None
    """

    import argparse
    import torch
    import math
    import util.plyobj as plyobj
    from util.image import save_image, save_fits
    from net.renderer import Splat
    from util.math import TransTen, PointsTen, VecRot

    parser = argparse.ArgumentParser(description="Render an image.")
   
    parser.add_argument(
        "--sigma",
        type=float,
        default=1.8,
        help="sigma to learn from (default: 1.8)",
    )

    parser.add_argument(
        "--obj",
        help="The object file to render",
    )

    parser.add_argument(
        "--rot",
        help="The object file to render",
    )

    args = parser.parse_args()
    use_cuda = False
    device = torch.device("cuda" if use_cuda else "cpu")
    base_points = PointsTen(device=device)
    base_points.from_points(plyobj.load_obj(args.obj))

    mask = []
    for _ in range(len(base_points)):
        mask.append(1.0)

    mask = torch.tensor(mask, device=device)
    xt = torch.tensor([0.0], dtype=torch.float32)
    yt = torch.tensor([0.0], dtype=torch.float32)

    splat = Splat(math.radians(90), 1.0, 1.0, 10.0, device=device)
    r = VecRot(0, 0, 0).to_ten(device=device)

    if args.rot is not None:
        tokens = args.rot.split(",")
        assert(len(tokens) == 3)
        r = VecRot(float(tokens[0]), float(tokens[1]), float(tokens[2])).to_ten(device=device)

    t = TransTen(xt, yt)
    model = splat.render(base_points, r, t, mask, sigma=1.8)
    save_image(model, name="renderer.jpg")
    save_fits(model, name="renderer.fits")