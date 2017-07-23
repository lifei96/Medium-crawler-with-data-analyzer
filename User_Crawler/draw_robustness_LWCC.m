function draw_robustness_LWCC()
    Y = [0.0479544111031,0.00179388702787,0.950251701869; 0.0701827505238,0.00217600017862,0.927641249298; 0.123758946475,0.00367622209038,0.872564831435; 0.186053587221,0.00706917736924,0.80687723541; 0.238819271261,0.0118516912179,0.749329037521; 0.350612869386,0.0397659351268,0.609621195487; 0.473041958924,0.110646862872,0.416311178204; 0.603534751158,0.212690717019,0.183774531824; 0.734012773424,0.26577346875,0.000213757825395];
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
    legend('Singletons', 'Middle region', 'LWCC', 'Location', 'NorthWest');
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/graph/robustness_LWCC.eps', '-depsc')
end