function draw_robustness_LSCC()
    Y = [0.0479544111031,0.188213139804,0.763832449093; 0.0701827505238,0.176406725041,0.753410524436; 0.123758946475,0.153577088012,0.722663965513; 0.186053587221,0.14868458125,0.665261831529; 0.238819271261,0.162690458857,0.598490269882; 0.350612869386,0.211723690065,0.437663440549; 0.473041958924,0.215434638583,0.311523402493; 0.603534751158,0.245456094425,0.151009154417; 0.734012773424,0.265858971881,0.000128254695237];
    X = {'0.01%', '0.1%', '1%', '5%', '10%', '20%', '30%', '40%', '50%'};
    bar(Y, 0.6, 'stacked');
    colormap(copper);
    xlim([0.5 9.5]);
    ylim([0 1]);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'xticklabel', X);
    set(gca, 'FontSize', 12);
    xlabel('Fraction of Network Removed','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    legend('Singletons', 'Middle region', 'LSCC', 'Location', 'NorthWest');
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/graph/robustness_LSCC.eps', '-depsc')
end